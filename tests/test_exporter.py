import tempfile
import unittest
from pathlib import Path
from utils.exporter import export_data

class TestExporter(unittest.TestCase):
    def test_json_export(self):
        with tempfile.TemporaryDirectory() as d:
            out = export_data([{"a": 1}], Path(d) / "x.json")
            self.assertTrue(out.exists())
            self.assertIn('"a": 1', out.read_text())

if __name__ == "__main__":
    unittest.main()
