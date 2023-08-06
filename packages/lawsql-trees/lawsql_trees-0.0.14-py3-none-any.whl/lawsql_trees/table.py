from datetime import date

from dateutil.parser import parse
from lawsql_utils.files import extract_statutes_details_only
from sqlite_utils import Database
from sqlite_utils.db import Table


def clean_rows():
    for detail in extract_statutes_details_only():
        yield {
            "cat": detail["category"].upper(),
            "idx": str(detail["numeral"]).upper(),
            "title": detail["law_title"],
            "date": (date_obj := parse(detail["date"]).date()),
            "year": date_obj.year,
            "month": date_obj.month,
        }


def create_statutes_tbl(db: Database, table_name: str) -> Table:
    tbl = db[table_name]
    tbl.create(
        columns={
            "cat": str,
            "idx": str,
            "title": str,
            "month": int,
            "year": int,
            "date": date,
        },
        pk=("cat", "idx"),
    )

    for i in [
        "cat",
        "idx",
        "year",
        "date",
        "title",
    ]:
        tbl.create_index([i])
    tbl.enable_fts(["title"], create_triggers=True)
    if not tbl.has_counts_triggers:
        tbl.enable_counts()
    return tbl.insert_all(clean_rows(), ignore=True)


def get_statutes_tbl():
    from .utils import get_db

    db = get_db("PATH_TO_DB_PROPER")
    if not db:
        raise ("Could not find proper database.")
    if not db["Statutes"].exists():
        return create_statutes_tbl(db, "Statutes")
    return db["Statutes"].insert_all(clean_rows(), ignore=True)
