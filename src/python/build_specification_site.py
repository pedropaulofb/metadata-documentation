"""Build the latest HTML specification and retain versioned snapshots."""

import argparse
import re
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
DOCS_URL = "https://w3id.org/health-ri/metadata/docs"
VERSION_RE = re.compile(r"v\d+\.\d+\.\d+")
REVISION_META_RE = re.compile(rb'<meta content="[0-9a-f]{40}" name="revision">')


class AssetReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        key = "src" if tag in {"img", "script"} else "href"
        if tag not in {"img", "script", "link", "a"}:
            return
        url = urlsplit(attributes.get(key, ""))
        if tag == "a" and Path(url.path).suffix.lower() not in {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".webp",
        }:
            return
        if not url.scheme and not url.netloc and url.path:
            self.paths.add(Path(unquote(url.path)))


def asset_paths(html):
    parser = AssetReferences()
    parser.feed(html.read_text(encoding="utf-8"))
    return parser.paths


def version_metadata(index):
    text = index.read_text(encoding="utf-8")

    def field(name):
        values = re.findall(rf"^{re.escape(name)}: (.+)$", text, re.MULTILINE)
        if len(values) != 1:
            raise ValueError(f"Expected exactly one {name} in {index}.")
        return values[0].strip()

    current = field("URL").removeprefix(DOCS_URL + "/")
    previous = field("Previous Version").removeprefix(DOCS_URL + "/")
    if not VERSION_RE.fullmatch(current) or not VERSION_RE.fullmatch(previous):
        raise ValueError(
            "URL and Previous Version must use versioned documentation PIDs."
        )
    if field("Canonical URL") != f"{DOCS_URL}/{current}" or field("TR") != DOCS_URL:
        raise ValueError(
            "Canonical URL and TR must identify the versioned and latest HTML specifications."
        )
    status_versions = re.findall(r"\bv\d+\.\d+\.\d+\b(?!\.\w)", field("Status Text"))
    if status_versions != [current]:
        raise ValueError("The document URL version must match Status Text.")
    if current == previous:
        raise ValueError("Previous Version must identify a different specification.")
    return current, previous


def files_in(directory):
    return {
        path.relative_to(directory): path
        for path in directory.rglob("*")
        if path.is_file()
    }


def same_snapshot(first, second, ignore_revision=False):
    left, right = files_in(first), files_in(second)
    if left.keys() != right.keys():
        return False
    for path in left:
        first_bytes, second_bytes = left[path].read_bytes(), right[path].read_bytes()
        if ignore_revision and path == Path("index.html"):
            first_bytes = REVISION_META_RE.sub(
                b'<meta name="revision">', first_bytes, count=1
            )
            second_bytes = REVISION_META_RE.sub(
                b'<meta name="revision">', second_bytes, count=1
            )
        if first_bytes != second_bytes:
            return False
    return True


def copy_archives(source, destination):
    if not source.is_dir():
        return
    for archive in source.iterdir():
        if not archive.is_dir() or not VERSION_RE.fullmatch(archive.name):
            continue
        target = destination / archive.name
        if not (archive / "index.html").is_file():
            raise ValueError(
                f"Archived specification is missing: {archive / 'index.html'}"
            )
        if target.exists():
            if not same_snapshot(archive, target):
                raise ValueError(
                    f"Conflicting archived specifications for {archive.name}."
                )
        else:
            shutil.copytree(archive, target)


def validate_assets(directory):
    for path in asset_paths(directory / "index.html"):
        target = (directory / path).resolve()
        if not target.is_relative_to(directory.resolve()) or not target.is_file():
            raise ValueError(f"Missing or invalid local asset: {directory / path}")


def build_site(root, output, published_site=None, bikeshed="bikeshed"):
    root, output = root.resolve(), output.resolve()
    current, previous = version_metadata(root / "index.bs")
    if output.exists():
        raise ValueError(f"Output already exists; choose a fresh directory: {output}")
    if published_site is not None and not published_site.is_dir():
        raise ValueError(f"Published site directory does not exist: {published_site}")

    with tempfile.TemporaryDirectory(prefix="health-ri-spec-") as temporary:
        staging = Path(temporary) / "site"
        archives = staging / "releases"
        archives.mkdir(parents=True)
        copy_archives(root / "releases", archives)
        if published_site is not None:
            copy_archives(published_site / "releases", archives)
        if not (archives / previous / "index.html").is_file():
            raise ValueError(f"Previous specification snapshot is missing: {previous}.")

        rendered = Path(temporary) / "current"
        rendered.mkdir()
        subprocess.run(
            [
                bikeshed,
                "--no-update",
                "spec",
                str(root / "index.bs"),
                str(rendered / "index.html"),
            ],
            cwd=root,
            check=True,
        )
        for path in asset_paths(rendered / "index.html"):
            source = (root / path).resolve()
            if not source.is_relative_to(root) or not source.is_file():
                raise ValueError(f"Missing or invalid source asset: {path}")
            target = rendered / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        snapshot = archives / current
        if snapshot.exists():
            if not same_snapshot(rendered, snapshot, ignore_revision=True):
                raise ValueError(
                    f"Published snapshot {current} differs from this build. "
                    "Keep published snapshots unchanged and use a new document version."
                )
            # Reuse the published HTML, including its original source revision.
            shutil.copyfile(snapshot / "index.html", rendered / "index.html")
        else:
            shutil.copytree(rendered, snapshot)
        shutil.copytree(rendered, staging, dirs_exist_ok=True)
        for archive in archives.iterdir():
            validate_assets(archive)
        validate_assets(staging)
        (staging / ".nojekyll").touch()
        shutil.copytree(staging, output)

    print(f"Latest specification: {output / 'index.html'}")
    print(f"This version: {output / 'releases' / current / 'index.html'}")
    print(f"Previous version: {output / 'releases' / previous / 'index.html'}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "_site",
        help="New output directory (default: repository _site).",
    )
    parser.add_argument(
        "--published-site",
        type=Path,
        help="Existing published site whose release snapshots must be retained.",
    )
    args = parser.parse_args(argv)
    try:
        build_site(ROOT, args.output, args.published_site)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Specification build failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
