"""Query validation, filtering and stable ordering."""
from operator import eq, ge, le, itemgetter

from validator import KEYS, valid_datetime

FILTERS = {
    "flight_id": ("flight_id", eq),
    "origin": ("origin", eq),
    "destination": ("destination", eq),
    "departure_datetime": ("departure_datetime", ge),
    "arrival_datetime": ("arrival_datetime", le),
    "price": ("price", le),
    "min_price": ("price", ge),
}


def valid_query(query: dict) -> bool:
    for key, value in query.items():
        if key in ("price", "min_price"):
            if type(value) not in (int, float):
                return False
        elif key == "limit":
            if type(value) is not int or value < 0:
                return False
        elif not isinstance(value, str):
            return False
        elif key == "sort_by":
            if value not in KEYS:
                return False
        elif key == "order":
            if "sort_by" not in query or value not in ("asc", "desc"):
                return False
        elif key in ("departure_datetime", "arrival_datetime"):
            if not valid_datetime(value):
                return False
        elif key not in FILTERS:
            return False
    return True


def run_query(db: list[dict], query: dict) -> dict:
    if not valid_query(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}
    conditions = [(field, compare, query[key]) for key, (field, compare) in FILTERS.items()
                  if key in query]
    matches = [row for row in db if all(compare(row[field], value)
                                         for field, compare, value in conditions)]
    if "sort_by" in query:
        matches.sort(key=itemgetter(query["sort_by"]), reverse=query.get("order") == "desc")
    return {"query": query, "matches": matches[:query.get("limit")]}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    if isinstance(queries, dict):
        queries = [queries]
    if not isinstance(queries, list) or not all(isinstance(q, dict) for q in queries):
        raise ValueError("expected a query object or array of query objects")
    return [run_query(db, q) for q in queries]
