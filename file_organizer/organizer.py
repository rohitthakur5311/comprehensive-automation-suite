from pathlib import Path
import hashlib
import shutil
from utils.logger import get_logger

logger = get_logger("file_organizer")

class FileOrganizer:
    def __init__(self, categories):
        self.categories = categories

    def category_for(self, path: Path):
        ext = path.suffix.lower()
        for category, extensions in self.categories.items():
            if ext in {e.lower() for e in extensions}:
                return category
        return "Other"

    @staticmethod
    def checksum(path, chunk_size=1024 * 1024):
        digest = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def organize(self, source, dry_run=True, recursive=False):
        source = Path(source).expanduser().resolve()
        if not source.is_dir():
            raise FileNotFoundError(f"Source directory not found: {source}")

        iterator = source.rglob("*") if recursive else source.glob("*")
        files = [p for p in iterator if p.is_file()]
        seen = {}
        results = []
        for path in files:
            category = self.category_for(path)
            target_dir = source / category
            target = target_dir / path.name
            checksum = None
            duplicate = False
            try:
                checksum = self.checksum(path)
                if checksum in seen:
                    duplicate = True
            except OSError as exc:
                logger.error("Checksum failed for %s: %s", path, exc)

            if not dry_run:
                target_dir.mkdir(exist_ok=True)
                if target.exists() and target.resolve() != path.resolve():
                    target = target_dir / f"{path.stem}_copy{path.suffix}"
                if target.resolve() != path.resolve():
                    shutil.move(str(path), str(target))

            if checksum:
                seen[checksum] = str(path)
            results.append({
                "file": str(path),
                "category": category,
                "duplicate": duplicate,
                "target": str(target),
            })
        logger.info("Processed %d files in %s", len(results), source)
        return results
