import tempfile
import unittest
from pathlib import Path
from file_organizer.organizer import FileOrganizer

class TestOrganizer(unittest.TestCase):
    def test_category(self):
        org = FileOrganizer({"Documents": [".pdf"], "Images": [".png"]})
        self.assertEqual(org.category_for(Path("report.pdf")), "Documents")
        self.assertEqual(org.category_for(Path("photo.png")), "Images")
        self.assertEqual(org.category_for(Path("x.xyz")), "Other")

    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.txt"
            p.write_text("hello")
            org = FileOrganizer({"Documents": [".txt"]})
            result = org.organize(d, dry_run=True)
            self.assertEqual(len(result), 1)
            self.assertTrue(p.exists())

if __name__ == "__main__":
    unittest.main()
