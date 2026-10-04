"""Offline release preflight against an explicitly selected schema checkout."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(schema):
    expected = json.loads((schema / 'Documents/next-release-properties.json').read_text())
    actual = json.loads((ROOT / 'src/next-release-properties.json').read_text())
    if actual != expected:
        raise SystemExit('Schema/documentation property manifests differ; review and synchronize them.')
    print('Schema and documentation property manifests match, including vocabulary provenance.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('schema_checkout', type=Path)
    check(parser.parse_args().schema_checkout)
