"""Read schedules in caller-supplied order."""
import csv
from pathlib import Path

from validator import to_record, validate_row


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    records, errors = [], []
    seen = set()
    for path in map(Path, paths):
        with path.open(encoding="utf-8", newline="") as source:
            next(source, None)
            for number, line in enumerate(source, start=2):
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue
                fields = next(csv.reader([line]))
                error = validate_row(fields, airports)
                if error is None:
                    record = to_record(fields)
                    key = record["flight_id"], record["departure_datetime"]
                    if key not in seen:
                        records.append(record)
                        seen.add(key)
                        continue
                    error = "DUPLICATE_FLIGHT"
                errors.append(f"{path.name}:{number}: {error} | {raw}")
    return records, errors
