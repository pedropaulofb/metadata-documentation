#!/usr/bin/env python3
"""Validate consistency of current-release version references."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]

INDEX = ROOT / "index.bs"
INTRO = ROOT / "src/chapter/4-introduction.md"

STATUS_RE = re.compile(
    r"^Status Text:.*\bv(?P<version>\d+\.\d+\.\d+)\b.*$"
)
UML_HEADING_RE = re.compile(
    r"^## UML Class Diagram v(?P<version>\d+\.\d+\.\d+)(?:\s+##\s+\{#[^ }]+\})?\s*$"
)
IMAGE_RE = re.compile(
    r"(?<![\w/.-])(?P<path>src/images/HRI_metadata_"
    r"(?P<version>V\d+\.\d+|p\d+_\d+)\.png)(?=$|[\s\"'<>\)\]])"
)


def matches_in_file(path, pattern):
    matches = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = pattern.search(line)
        if match:
            matches.append((line_number, match))
    return matches


def main():
    errors = []
    full_versions = []

    def require_one(path, pattern, label):
        matches = matches_in_file(path, pattern)
        rel = path.relative_to(ROOT)
        if len(matches) != 1:
            errors.append(
                f"{rel}: expected exactly one {label}; found {len(matches)}."
            )
            return None

        line_number, match = matches[0]
        full_versions.append(
            {
                "label": label,
                "file": str(rel),
                "line": line_number,
                "value": match.group("version"),
            }
        )
        return match

    require_one(INDEX, STATUS_RE, "Bikeshed status version")
    require_one(INTRO, UML_HEADING_RE, "UML heading version")

    image_matches = matches_in_file(INTRO, IMAGE_RE)
    images = []
    if not image_matches:
        errors.append(
            f"{INTRO.relative_to(ROOT)}: expected at least one versioned UML image reference; found 0."
        )
    else:
        for line_number, match in image_matches:
            images.append(
                {
                    "label": "UML image version",
                    "file": str(INTRO.relative_to(ROOT)),
                    "line": line_number,
                    # Current V2.1 and legacy p2_1 names both encode major/minor.
                    "value": match.group("version")[1:].replace("_", "."),
                    "path": match.group("path"),
                }
            )

    if len(full_versions) == 2:
        versions = {item["value"] for item in full_versions}
        if len(versions) != 1:
            details = "; ".join(
                f'{item["file"]}:{item["line"]} = {item["value"]}'
                for item in full_versions
            )
            errors.append(f"Full-version mismatch: {details}.")
        else:
            full_version = full_versions[0]["value"]
            expected_major_minor = ".".join(full_version.split(".")[:2])
            for image in images:
                if image["value"] != expected_major_minor:
                    errors.append(
                        "Major/minor mismatch: "
                        f'{image["file"]}:{image["line"]} references {image["path"]} '
                        f'(version {image["value"]}), but the full current version is '
                        f"{full_version} (expected image version {expected_major_minor})."
                    )

    checked_image_paths = set()
    for image in images:
        if image["path"] in checked_image_paths:
            continue
        checked_image_paths.add(image["path"])

        image_path = ROOT / image["path"]
        if not image_path.is_file():
            errors.append(
                f'{image["file"]}:{image["line"]}: referenced UML image does not exist: '
                f'{image["path"]}.'
            )

    print("Current-release version references:")
    for item in full_versions:
        print(
            f'  {item["label"]}: {item["value"]} '
            f'({item["file"]}:{item["line"]})'
        )
    for item in images:
        print(
            f'  {item["label"]}: {item["value"]} '
            f'({item["file"]}:{item["line"]} -> {item["path"]})'
        )

    if errors:
        print("\nVersion consistency check FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("\nVersion consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
