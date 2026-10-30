"""Version checker regression tests using temporary documentation fixtures."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/python/check_version_consistency.py"
SPEC = importlib.util.spec_from_file_location("version_checker", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class VersionConsistencyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.index = self.root / "index.bs"
        self.intro = self.root / "src/chapter/4-introduction.md"
        self.intro.parent.mkdir(parents=True)
        self.image = "src/images/HRI_metadata_V2.1.png"
        self.index.write_text(
            "Status Text: Health-RI core metadata schema v2.1.0.\n",
            encoding="utf-8",
        )
        self.write_intro()
        self.create_image(self.image)
        patches = patch.multiple(
            checker, ROOT=self.root, INDEX=self.index, INTRO=self.intro,
        )
        patches.start()
        self.addCleanup(patches.stop)

    def write_intro(self, version="2.1.0", image=None, anchored=True):
        heading = f"## UML Class Diagram v{version}"
        if anchored:
            heading += " ## {#uml-class-diagram}"
        image = self.image if image is None else image
        self.intro.write_text(
            f'{heading}\n\n<a href="{image}">\n<img src="{image}">\n</a>\n',
            encoding="utf-8",
        )

    def create_image(self, relative_path):
        image = self.root / relative_path
        image.parent.mkdir(parents=True, exist_ok=True)
        # The checker validates the referenced path, not PNG contents.
        image.touch()

    def validate(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = checker.main()
        return status, stdout.getvalue(), stderr.getvalue()

    def assert_valid(self):
        status, stdout, stderr = self.validate()
        self.assertEqual(status, 0, stderr)
        self.assertIn("Version consistency check passed.", stdout)
        self.assertEqual(stderr, "")
        return stdout

    def assert_invalid(self, message):
        status, stdout, stderr = self.validate()
        self.assertEqual(status, 1)
        self.assertIn("Version consistency check FAILED:", stderr)
        self.assertIn(message, stderr)
        self.assertNotIn("Version consistency check passed.", stdout)
        return stderr

    def test_matching_versions_and_current_image_format_pass(self):
        stdout = self.assert_valid()
        self.assertIn("Bikeshed status version: 2.1.0", stdout)
        self.assertIn("UML heading version: 2.1.0", stdout)
        self.assertIn("UML image version: 2.1", stdout)

    def test_legacy_image_format_remains_supported(self):
        image = "src/images/HRI_metadata_p2_1.png"
        self.create_image(image)
        self.write_intro(image=image)
        self.assertIn("UML image version: 2.1", self.assert_valid())

    def test_original_uml_heading_without_explicit_anchor_remains_supported(self):
        self.write_intro(anchored=False)
        self.assert_valid()

    def test_image_does_not_need_a_patch_version(self):
        self.index.write_text("Status Text: Schema v2.1.7.\n", encoding="utf-8")
        self.write_intro(version="2.1.7")
        self.assert_valid()

    def test_current_generator_and_arbitrary_workbook_names_are_not_version_inputs(self):
        scripts = self.root / "src/python"
        scripts.mkdir()
        shutil.copyfile(ROOT / "src/python/Excel_To_Html.py", scripts / "Excel_To_Html.py")
        excel = self.root / "src/excel"
        excel.mkdir()
        # These are not opened or selected by the documentation version checker.
        for filename in ["arbitrary workbook.xlsx", "HealthRI_v99.0.0.xlsx"]:
            (excel / filename).touch()
        self.assert_valid()

    def test_full_version_mismatch_is_rejected_including_patch_difference(self):
        self.write_intro(version="2.1.1")
        stderr = self.assert_invalid("Full-version mismatch:")
        self.assertIn("2.1.0", stderr)
        self.assertIn("2.1.1", stderr)

    def test_wrong_image_major_or_minor_version_is_rejected_for_both_formats(self):
        for filename in [
            "HRI_metadata_V3.1.png", "HRI_metadata_V2.2.png",
            "HRI_metadata_p3_1.png", "HRI_metadata_p2_2.png",
        ]:
            with self.subTest(filename=filename):
                image = f"src/images/{filename}"
                self.create_image(image)
                self.write_intro(image=image)
                stderr = self.assert_invalid("Major/minor mismatch:")
                self.assertIn(image, stderr)
                self.assertIn("expected image version 2.1", stderr)

    def test_missing_image_reference_is_rejected(self):
        self.intro.write_text("## UML Class Diagram v2.1.0\n", encoding="utf-8")
        self.assert_invalid("expected at least one versioned UML image reference; found 0")

    def test_unrecognized_image_filenames_are_rejected_even_when_files_exist(self):
        for filename in [
            "HRI_metadata_V2.png", "HRI_metadata_V2.x.png",
            "HRI_metadata_V2.1.0.png", "HRI_metadata_V2_1.png",
            "HRI_metadata_p2.1.png", "HRI_metadata_V2.1.jpg",
            "HRI_metadata_V2.1.png.bak", "HRI_metadata_V2.1.png-extra",
            "Other_metadata_V2.1.png",
        ]:
            with self.subTest(filename=filename):
                image = f"src/images/{filename}"
                self.create_image(image)
                self.write_intro(image=image)
                self.assert_invalid(
                    "expected at least one versioned UML image reference; found 0"
                )

    def test_missing_referenced_image_is_rejected(self):
        (self.root / self.image).unlink()
        self.assert_invalid(f"referenced UML image does not exist: {self.image}")

    def test_image_directory_is_not_accepted_as_a_file(self):
        image = self.root / self.image
        image.unlink()
        image.mkdir()
        self.assert_invalid(f"referenced UML image does not exist: {self.image}")

    def test_additional_mismatched_image_reference_is_not_ignored(self):
        image = "src/images/HRI_metadata_V2.2.png"
        self.create_image(image)
        with self.intro.open("a", encoding="utf-8") as stream:
            stream.write(f'<img src="{image}">\n')
        self.assert_invalid("Major/minor mismatch:")

    def test_additional_missing_image_reference_is_not_ignored(self):
        image = "src/images/HRI_metadata_p2_1.png"
        with self.intro.open("a", encoding="utf-8") as stream:
            stream.write(f'<img src="{image}">\n')
        self.assert_invalid(f"referenced UML image does not exist: {image}")

    def test_image_references_on_the_same_line_are_all_checked(self):
        for image, exists, message in [
            ("src/images/HRI_metadata_V2.2.png", True, "Major/minor mismatch:"),
            ("src/images/HRI_metadata_p2_1.png", False, "referenced UML image does not exist:"),
        ]:
            with self.subTest(image=image):
                if exists:
                    self.create_image(image)
                self.intro.write_text(
                    "## UML Class Diagram v2.1.0\n\n"
                    f'<a href="{self.image}"><img src="{image}"></a>\n',
                    encoding="utf-8",
                )
                self.assert_invalid(message)

    def test_missing_required_full_versions_are_rejected(self):
        for path, label in [
            (self.index, "Bikeshed status version"),
            (self.intro, "UML heading version"),
        ]:
            with self.subTest(label=label):
                original = path.read_text(encoding="utf-8")
                path.write_text("", encoding="utf-8")
                self.assert_invalid(f"expected exactly one {label}; found 0")
                path.write_text(original, encoding="utf-8")

    def test_invalid_required_full_versions_are_rejected(self):
        for path, label in [
            (self.index, "Bikeshed status version"),
            (self.intro, "UML heading version"),
        ]:
            original = path.read_text(encoding="utf-8")
            for version in ["2.1", "2.1.x", "2.1.0.9", "2.1.0.x", "unknown"]:
                with self.subTest(label=label, version=version):
                    path.write_text(original.replace("2.1.0", version), encoding="utf-8")
                    self.assert_invalid(f"expected exactly one {label}; found 0")
            path.write_text(original, encoding="utf-8")

    def test_duplicate_required_full_versions_are_rejected(self):
        for path, label in [
            (self.index, "Bikeshed status version"),
            (self.intro, "UML heading version"),
        ]:
            with self.subTest(label=label):
                original = path.read_text(encoding="utf-8")
                path.write_text(original + original, encoding="utf-8")
                self.assert_invalid(f"expected exactly one {label}; found 2")
                path.write_text(original, encoding="utf-8")

    def run_command(self):
        script = self.root / "src/python/check_version_consistency.py"
        script.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SCRIPT, script)
        return subprocess.run(
            [sys.executable, "-B", str(script)], cwd=self.root / "src",
            capture_output=True, text=True,
        )

    def test_cli_works_from_another_working_directory_without_excel_files(self):
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Version consistency check passed.", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_cli_reports_failure_and_returns_nonzero_for_inconsistent_versions(self):
        self.write_intro(version="2.1.1")
        result = self.run_command()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Full-version mismatch:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
