import os
from pathlib import Path
from typing import Iterator

from citation_decision import CitationDocument, RawCitation
from dotenv import find_dotenv, load_dotenv
from lawsql_utils.files.path_to_local import get_path
from sqlite_utils import Database

db = Database(get_path("PATH_TO_DB_PROPER"))


def format_citations(nodes: list[dict]) -> None:
    for node in nodes:
        if histories := node.get("history", None):
            for history in histories:
                if history.get("citation", None):
                    doc = CitationDocument(history["citation"])
                    history["citation"] = doc.first_canonical
        if new_nodes := node.get("units", None):
            format_citations(new_nodes)  # call self


def identify_citation(r: RawCitation, db: Database) -> Iterator:
    cols = "source, pk"
    if r.docket is not None:
        if r.model.short_category:
            q = "cat = ? and idx = ? and date_prom = date(?)"
            params = (
                r.model.short_category.lower(),
                r.model.cleaned_ids.lower(),
                r.model.docket_date.isoformat(),
            )
            return db["Decisions"].rows_where(q, params, select=cols)
    if r.scra is not None:
        params = (r.scra,)
        return db["Decisions"].rows_where("scra = ?", params, select=cols)
    if r.phil is not None:
        params = (r.phil,)
        return db["Decisions"].rows_where("phil = ?", params, select=cols)
    if r.offg is not None:
        params = (r.offg,)
        return db["Decisions"].rows_where("offg = ?", params, select=cols)
    return None


def get_citation(text: str) -> dict | None:
    try:
        raw: RawCitation = CitationDocument(text).first
    except:
        return None

    try:
        if rows := identify_citation(raw, db):
            return next(rows) | {"raw": raw}
    except:
        ...
    return None
