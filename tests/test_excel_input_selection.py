"""Workbook selection tests; all generated files stay in temporary directories."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from openpyxl import Workbook


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src/python/Excel_To_Html.py"
SPEC = importlib.util.spec_from_file_location("excel_generator", SCRIPT)
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class WorkbookSelectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.excel = self.root / "src/excel"
        self.excel.mkdir(parents=True)
        self.output = self.root / "src/property"
        patches = patch.multiple(
            generator, ROOT=self.root, EXCEL_DIRECTORY=self.excel,
            OUTPUT_PATH=self.output,
        )
        patches.start()
        self.addCleanup(patches.stop)

    def candidate(self, name, modified=1_700_000_000_000_000_001):
        path = self.excel / name
        path.write_bytes(b"Selection tests do not need workbook contents.")
        os.utime(path, ns=(modified, modified))
        return path

    def assert_cli_error(self, args, message):
        stderr = io.StringIO()
        with redirect_stderr(stderr), redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                generator.main(args)
        self.assertEqual(error.exception.code, 2)
        self.assertIn(message, stderr.getvalue())
        self.assertFalse(self.output.exists())

    def test_explicit_selection_overrides_newer_workbook(self):
        selected = self.candidate("older.xlsx")
        self.candidate("newer.xlsx", selected.stat().st_mtime_ns + 1)
        self.assertEqual(generator.select_workbook(str(selected)), selected)

    def test_relative_paths_are_repository_relative(self):
        selected = self.candidate("relative.xlsx")
        self.assertEqual(
            generator.select_workbook("src/excel/relative.xlsx"), selected
        )

    def test_absolute_path_can_be_outside_excel_directory(self):
        selected = self.root / "outside.xlsx"
        selected.write_bytes(b"Workbook candidate")
        self.assertEqual(generator.select_workbook(str(selected)), selected)

    def test_latest_timestamp_wins_regardless_of_name_or_version(self):
        self.candidate("HealthRI_v99.0.0.xlsx")
        selected = self.candidate("arbitrary name.xlsx", 1_700_000_000_000_000_002)
        self.assertEqual(generator.select_workbook(), selected)

    def test_extension_is_case_insensitive(self):
        self.candidate("old.xlsx")
        selected = self.candidate("new.XlSx", 1_700_000_000_000_000_002)
        self.assertEqual(generator.select_workbook(), selected)

    def test_lock_files_non_xlsx_files_and_directories_are_ignored(self):
        selected = self.candidate("eligible.xlsx")
        self.candidate("~$locked.XLSX", 1_700_000_000_000_000_002)
        self.candidate("other.xls", 1_700_000_000_000_000_003)
        (self.excel / "directory.xlsx").mkdir()
        self.assertEqual(generator.select_workbook(), selected)

    def test_only_top_level_workbooks_are_candidates(self):
        selected = self.candidate("eligible.xlsx")
        nested = self.excel / "nested"
        nested.mkdir()
        (nested / "newer.xlsx").write_bytes(b"Not a direct candidate")
        self.assertEqual(generator.select_workbook(), selected)

    def test_empty_directory_produces_helpful_error(self):
        self.assert_cli_error([], "No eligible .xlsx workbooks")

    def test_directory_with_only_ineligible_entries_is_empty_for_selection(self):
        self.candidate("~$locked.xlsx")
        self.candidate("notes.txt")
        (self.excel / "directory.xlsx").mkdir()
        self.assert_cli_error([], "No eligible .xlsx workbooks")

    def test_missing_excel_directory_produces_selection_error(self):
        self.excel.rmdir()
        self.assert_cli_error([], "Cannot select Excel workbook")

    def test_missing_explicit_path_does_not_fall_back(self):
        self.candidate("available.xlsx")
        self.assert_cli_error(["--excel", "missing.xlsx"], "Workbook does not exist")

    def test_explicit_directory_is_rejected(self):
        self.assert_cli_error(["--excel", str(self.excel)], "points to a directory")

    def test_highest_timestamp_tie_requires_explicit_selection(self):
        first = self.candidate("first.xlsx")
        self.candidate("second.xlsx")
        self.assert_cli_error([], "Use --excel PATH")
        self.assertEqual(generator.select_workbook(str(first)), first)

    def test_ties_at_older_timestamps_do_not_prevent_selection(self):
        self.candidate("old-one.xlsx")
        self.candidate("old-two.xlsx")
        selected = self.candidate("latest.xlsx", 1_700_000_000_000_000_002)
        self.assertEqual(generator.select_workbook(), selected)

    def test_corrupt_workbook_produces_read_error_without_fallback(self):
        selected = self.candidate("corrupt.xlsx")
        self.assert_cli_error(["--excel", str(selected)], "Cannot read workbook")

    def test_permission_error_produces_read_error(self):
        selected = self.candidate("unreadable.xlsx")
        with patch.object(generator.pd, "read_excel", side_effect=PermissionError("Access denied")):
            self.assert_cli_error(["--excel", str(selected)], "Access denied")


class GeneratorCommandTests(unittest.TestCase):
    def test_modes_and_output_location_from_different_working_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            scripts = root / "src/python"
            scripts.mkdir(parents=True)
            script = scripts / SCRIPT.name
            shutil.copyfile(SCRIPT, script)
            shutil.copyfile(SCRIPT.with_name("links.json"), scripts / "links.json")
            excel = root / "src/excel"
            excel.mkdir()
            workbook = excel / "arbitrary workbook.XLSX"
            wb = Workbook()
            classes = wb.active
            classes.title = "classes"
            classes.append(["sheet_name"])
            classes.append(["Dataset"])
            dataset = wb.create_sheet("Dataset")
            dataset.append([
                "Property label", "Definition", "Property URI", "Range",
                "Cardinality", "Usage note", "Controlled vocabluary (if applicable)",
            ])
            dataset.append([
                "Example", "Example definition", "ex:example", "rdfs:Literal",
                "0..*", "Example usage", "Example vocabulary",
            ])
            dataset["G2"].hyperlink = "https://example.org/vocabulary"
            wb.save(workbook)
            wb.close()
            output = root / "src/property/properties-dataset.html"
            cases = [
                (["--excel", "src/excel/arbitrary workbook.XLSX"], "Explicit"),
                (["--excel", str(workbook)], "Explicit"),
                ([], "Automatic (most recently modified)"),
            ]
            for cwd in [root, scripts, Path(temporary)]:
                for args, mode in cases:
                    with self.subTest(cwd=cwd, args=args):
                        result = subprocess.run(
                            [sys.executable, "-B", str(script), *args], cwd=cwd,
                            capture_output=True, text=True,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn(f"Excel input mode: {mode}", result.stdout)
                        self.assertIn(f"Selected workbook: {workbook}", result.stdout)
                        self.assertTrue(output.is_file())
                        self.assertIn("https://example.org/vocabulary", output.read_text())
                        output.unlink()


if __name__ == "__main__":
    unittest.main()
