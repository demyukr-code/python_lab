"""Validation and normalization of schedule rows."""
import math
import re
from datetime import datetime

KEYS = ("flight_id", "origin", "destination", "departure_datetime", "arrival_datetime", "price")


def load_airports(path: str) -> set[str]:
    with open(path, encoding="utf-8") as source:
        return {code for line in source if (code := line.strip()) and not code.startswith("#")}


def valid_datetime(value: str) -> bool:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", value):
        return False
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"
    values = [field.strip() for field in fields]
    if "" in values:
        return "MISSING_FIELD"
    flight, origin, destination, departure, arrival, price = values
    if not re.fullmatch(r"[A-Za-z0-9]{2,8}", flight):
        return "INVALID_FLIGHT_ID"
    if origin not in airports or not re.fullmatch(r"[A-Z]{3}", origin):
        return "INVALID_ORIGIN"
    if destination not in airports or not re.fullmatch(r"[A-Z]{3}", destination):
        return "INVALID_DESTINATION"
    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"
    if not valid_datetime(departure):
        return "INVALID_DEPARTURE"
    if not valid_datetime(arrival):
        return "INVALID_ARRIVAL"
    if arrival <= departure:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"
    try:
        amount = float(price)
    except ValueError:
        return "INVALID_PRICE"
    if not math.isfinite(amount):
        return "INVALID_PRICE"
    if amount <= 0:
        return "NON_POSITIVE_PRICE"
    return None


def to_record(fields: list[str]) -> dict:
    record = dict(zip(KEYS, (field.strip() for field in fields), strict=True))
    record["price"] = float(record["price"])
    return record
