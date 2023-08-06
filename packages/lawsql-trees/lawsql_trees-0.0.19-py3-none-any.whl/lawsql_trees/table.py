import os
from datetime import date
from pathlib import Path
from typing import Iterator

import yaml
from dateutil.parser import parse
from dotenv import find_dotenv, load_dotenv
from sqlite_utils import Database
from sqlite_utils.db import Table

from .utils import DB_FILE

load_dotenv(find_dotenv())


def clean_rows():
    paths = (
        Path().home().joinpath(os.getenv("STATUTES")).glob("**/details.yaml")
    )
    for path in paths:
        detail = yaml.load(path.read_text(), Loader=yaml.SafeLoader)
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
    if not DB_FILE:
        raise ("Could not find proper database.")
    if not DB_FILE["Statutes"].exists():
        return create_statutes_tbl(DB_FILE, "Statutes")
    return DB_FILE["Statutes"].insert_all(clean_rows(), ignore=True)
