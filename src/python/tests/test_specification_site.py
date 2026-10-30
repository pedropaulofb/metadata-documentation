"""Versioned publication tests using temporary HTML and image fixtures."""

import importlib.util
import io
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "specification_site", ROOT / "src/python/build_specification_site.py"
)
site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(site)


class SpecificationSiteTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "source"
        self.root.mkdir()
        self.output = self.root.parent / "output"
        self.published = self.root.parent / "published"
        self.published.mkdir()
        self.write_metadata()
        self.previous = self.root / "releases/v2.0.3"
        self.write_snapshot(self.previous, "Previous specification")
        image = self.root / "src/images/logo.png"
        image.parent.mkdir(parents=True)
        image.write_bytes(b"current image")
        self.html = (
            '<!doctype html><img src="src/images/logo.png"><p>Current specification</p>'
        )
        self.bikeshed = patch.object(site.subprocess, "run", side_effect=self.render)
        self.render_mock = self.bikeshed.start()
        self.addCleanup(self.bikeshed.stop)

    def write_metadata(self, current="v2.1.0", previous="v2.0.3"):
        (self.root / "index.bs").write_text(
            f"Status Text: Health-RI metadata schema {current}.\n"
            f"URL: {site.DOCS_URL}/{current}\n"
            f"Canonical URL: {site.DOCS_URL}/{current}\n"
            f"TR: {site.DOCS_URL}\n"
            f"Previous Version: {site.DOCS_URL}/{previous}\n",
            encoding="utf-8",
        )

    def write_snapshot(self, directory, text):
        directory.mkdir(parents=True)
        (directory / "index.html").write_text(
            f'<img src="logo.png"><p>{text}</p>', encoding="utf-8"
        )
        (directory / "logo.png").write_bytes(b"archived image")

    def render(self, command, **kwargs):
        self.assertEqual(kwargs, {"cwd": self.root, "check": True})
        self.assertEqual(
            command[1:4], ["--no-update", "spec", str(self.root / "index.bs")]
        )
        Path(command[-1]).write_text(self.html, encoding="utf-8")

    def build(self, published=False):
        with redirect_stdout(io.StringIO()):
            site.build_site(
                self.root, self.output, self.published if published else None
            )

    def test_existing_document_hyperlinks_are_not_treated_as_embedded_assets(self):
        self.html += (
            '<a href="Documents/previous-workbook.xlsx">Existing workbook link</a>'
        )
        self.build()
        self.assertEqual((self.output / "index.html").read_text(), self.html)

    def test_latest_and_current_snapshot_match_and_previous_is_preserved(self):
        before = {
            path: file.read_bytes()
            for path, file in site.files_in(self.previous).items()
        }
        self.build()
        current = self.output / "releases/v2.1.0"
        self.assertEqual((self.output / "index.html").read_text(), self.html)
        self.assertEqual((current / "index.html").read_text(), self.html)
        self.assertEqual(
            (current / "src/images/logo.png").read_bytes(), b"current image"
        )
        self.assertEqual(
            (self.output / "src/images/logo.png").read_bytes(), b"current image"
        )
        for path, contents in before.items():
            self.assertEqual(
                (self.output / "releases/v2.0.3" / path).read_bytes(), contents
            )
            self.assertEqual((self.previous / path).read_bytes(), contents)
        self.assertTrue((self.output / ".nojekyll").is_file())

    def test_older_published_snapshots_are_retained(self):
        archive = self.published / "releases/v1.0.1"
        self.write_snapshot(archive, "Older specification")
        self.build(published=True)
        self.assertTrue(site.same_snapshot(archive, self.output / "releases/v1.0.1"))

    def test_identical_existing_current_snapshot_is_accepted(self):
        self.build()
        shutil.copytree(self.output / "releases", self.published / "releases")
        shutil.rmtree(self.output)
        self.build(published=True)
        self.assertTrue(
            site.same_snapshot(
                self.published / "releases/v2.1.0", self.output / "releases/v2.1.0"
            )
        )

    def test_changed_existing_current_snapshot_is_rejected(self):
        self.write_snapshot(
            self.published / "releases/v2.1.0", "Published current specification"
        )
        with self.assertRaisesRegex(ValueError, "Published snapshot v2.1.0 differs"):
            self.build(published=True)
        self.assertFalse(self.output.exists())

    def test_next_version_keeps_the_previous_current_snapshot(self):
        self.build()
        shutil.copytree(self.output / "releases", self.published / "releases")
        old_current = (self.output / "releases/v2.1.0/index.html").read_bytes()
        shutil.rmtree(self.output)
        self.write_metadata(current="v2.2.0", previous="v2.1.0")
        self.html += "<p>Next version</p>"
        self.build(published=True)
        self.assertEqual(
            (self.output / "releases/v2.1.0/index.html").read_bytes(), old_current
        )
        self.assertEqual(
            (self.output / "releases/v2.2.0/index.html").read_text(), self.html
        )

    def test_conflicting_historical_snapshots_are_rejected(self):
        self.write_snapshot(
            self.published / "releases/v2.0.3", "Different previous specification"
        )
        with self.assertRaisesRegex(ValueError, "Conflicting archived specifications"):
            self.build(published=True)
        self.render_mock.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_missing_previous_snapshot_is_rejected(self):
        shutil.rmtree(self.previous)
        with self.assertRaisesRegex(
            ValueError, "Previous specification snapshot is missing"
        ):
            self.build()
        self.render_mock.assert_not_called()

    def test_missing_archived_html_is_rejected(self):
        (self.previous / "index.html").unlink()
        with self.assertRaisesRegex(ValueError, "Archived specification is missing"):
            self.build()

    def test_missing_current_or_archived_images_are_rejected(self):
        for image in [self.root / "src/images/logo.png", self.previous / "logo.png"]:
            with self.subTest(image=image):
                contents = image.read_bytes()
                image.unlink()
                with self.assertRaisesRegex(ValueError, "Missing or invalid"):
                    self.build()
                self.assertFalse(self.output.exists())
                image.write_bytes(contents)

    def test_invalid_or_inconsistent_publication_metadata_is_rejected(self):
        original = (self.root / "index.bs").read_text()
        for old, new in [
            (f"TR: {site.DOCS_URL}", "TR: https://github.com/example/releases/latest"),
            (f"URL: {site.DOCS_URL}/v2.1.0", f"URL: {site.DOCS_URL}/v2.1"),
            ("schema v2.1.0.", "schema v2.2.0."),
            (f"Previous Version: {site.DOCS_URL}/v2.0.3", ""),
            (
                f"Previous Version: {site.DOCS_URL}/v2.0.3",
                f"Previous Version: {site.DOCS_URL}/v2.1.0",
            ),
        ]:
            with self.subTest(new=new):
                (self.root / "index.bs").write_text(original.replace(old, new))
                with self.assertRaises(ValueError):
                    self.build()
                self.assertFalse(self.output.exists())

    def test_bikeshed_failure_is_not_published(self):
        self.render_mock.side_effect = subprocess.CalledProcessError(1, "bikeshed")
        with self.assertRaises(subprocess.CalledProcessError):
            self.build()
        self.assertFalse(self.output.exists())

    def test_existing_output_is_not_overwritten(self):
        self.output.mkdir()
        sentinel = self.output / "keep.txt"
        sentinel.write_text("existing file")
        with self.assertRaisesRegex(ValueError, "Output already exists"):
            self.build()
        self.assertEqual(sentinel.read_text(), "existing file")

    def test_missing_published_site_is_rejected(self):
        self.published.rmdir()
        with self.assertRaisesRegex(
            ValueError, "Published site directory does not exist"
        ):
            self.build(published=True)

    def test_local_assets_cannot_escape_the_source_directory(self):
        self.html = '<img src="../outside.png">'
        (self.root.parent / "outside.png").write_bytes(b"outside")
        with self.assertRaisesRegex(ValueError, "Missing or invalid source asset"):
            self.build()
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
