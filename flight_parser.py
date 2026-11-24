"""Command-line flight schedule parser and query tool."""
import argparse
import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from csv_loader import parse_files
from query import run_queries
from validator import load_airports

STUDENT_ID = "251ADB152"
FIRST_NAME = "Kristina"
LAST_NAME = "Deminska"


def read_json(path):
    with open(path, encoding="utf-8") as source:
        return json.load(source, parse_constant=reject_constant)


def reject_constant(token):
    raise ValueError(f"invalid JSON constant {token}")


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as target:
        json.dump(data, target, indent=2)


def write_log(path, messages):
    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(path, mode="w", encoding="utf-8")
    try:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)
        for message in messages:
            logger.warning(message)
    finally:
        logger.removeHandler(handler)
        handler.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE", help="read one CSV schedule")
    source.add_argument("-d", metavar="FOLDER", help="read CSV schedules in filename order")
    source.add_argument("-j", metavar="FILE", help="load an existing JSON database")
    parser.add_argument("-a", metavar="FILE", help="airport list")
    parser.add_argument("-o", metavar="FILE", help="database output (default db.json)")
    parser.add_argument("-q", metavar="FILE", help="JSON queries")
    parser.add_argument("-r", metavar="FOLDER", default=".", help="response directory")
    try:
        args = parser.parse_args(argv)
        if args.j is None and args.a is None:
            parser.error("-a is required with -i or -d")
        if args.j is not None and args.o is not None:
            parser.error("-o cannot be used with -j")
    except SystemExit as exc:
        return int(exc.code)
    try:
        if args.j is not None:
            db = read_json(args.j)
            if not isinstance(db, list) or not all(isinstance(row, dict) for row in db):
                raise ValueError("expected an array of database records")
        else:
            paths = [args.i]
            if args.d is not None:
                paths = sorted(str(p) for p in Path(args.d).iterdir()
                               if p.name.endswith(".csv") and p.is_file())
                if not paths:
                    raise ValueError("no .csv files in folder")
            db, errors = parse_files(paths, load_airports(args.a))
            output = Path(args.o if args.o is not None else "db.json")
            write_json(output, db)
            write_log(output.parent / "errors.log", errors)
        if args.q is not None:
            responses = run_queries(db, read_json(args.q))
            stamp = datetime.now().strftime("%Y%m%d_%H%M")
            name = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{stamp}.json"
            write_json(Path(args.r) / name, responses)
    except (OSError, ValueError, csv.Error, RecursionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
