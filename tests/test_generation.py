"""Protect generated property tables and intentional next-release additions."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generator', ROOT / 'src/python/Excel_To_Html.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class GenerationTests(unittest.TestCase):
    def test_tables_are_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            original = generator.OUTPUT_PATH
            try:
                generator.OUTPUT_PATH = Path(directory)
                generator.main()
                for generated in Path(directory).glob('*.html'):
                    self.assertEqual(generated.read_text(), (original / generated.name).read_text(), generated.name)
            finally:
                generator.OUTPUT_PATH = original

    def test_release_additions_and_endpoint_identifier(self):
        table = (ROOT / 'src/property/properties-dataset.html').read_text()
        manifest = json.loads((ROOT / 'src/next-release-properties.json').read_text())
        self.assertEqual(len(manifest['properties']), 5)
        for prop in manifest['properties']:
            self.assertEqual(table.count('<td>' + prop['curie'] + '</td>'), 1)
            self.assertIn(prop['definition'], table)
            self.assertEqual(prop['cardinality'], '0..n')
        service = (ROOT / 'src/property/properties-dataservice.html').read_text()
        self.assertIn('<td>dcat:endpointURL</td>', service)
        self.assertNotIn('dcat:endPointURL', service)


if __name__ == '__main__':
    unittest.main()
