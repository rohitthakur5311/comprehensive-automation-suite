"""CSV, JSON and XLSX export helpers."""
import csv
import json
from pathlib import Path

def export_data(rows, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    ext = output.suffix.lower()
    if ext == ".json":
        output.write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")
    elif ext == ".csv":
        keys = sorted({k for row in rows for k in row.keys()}) if rows else []
        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
    elif ext == ".xlsx":
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        keys = sorted({k for row in rows for k in row.keys()}) if rows else []
        ws.append(keys)
        for row in rows:
            ws.append([row.get(k, "") for k in keys])
        wb.save(output)
    else:
        raise ValueError("Supported formats: .csv, .json, .xlsx")
    return output
