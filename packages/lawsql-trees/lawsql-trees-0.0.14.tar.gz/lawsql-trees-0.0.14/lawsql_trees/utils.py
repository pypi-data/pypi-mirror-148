import os
from pathlib import Path
from typing import Iterator

from citation_decision import CitationDocument, RawCitation
from dotenv import find_dotenv, load_dotenv
from sqlite_utils import Database


def get_db(env_var: str) -> Database | None:
    load_dotenv(find_dotenv())
    if paths := os.getenv(env_var, None):
        path = Path().home().joinpath(paths)
        if path.exists():
            return Database(path)
    return None


db = get_db("PATH_TO_DB_PROPER")


def set_tree_ids(nodes: list[dict], parent_id: str = "1"):
    """Recursive function updates  nodes in place since list/dicts are mutable.Adds an string id to each deeply nested json whereby each string id is in the following format: "1.1". If node id "1.1" has child nodes, the first child node will be "1.1.1". The root of the tree will always be "1".

    Args:
        nodes (list[dict]): Each dict in the list may have `units` key
        parent_id (str): This is the parent of the node being evaluated
    """
    for counter, node in enumerate(nodes, start=1):
        node["id"] = f"{parent_id}.{str(counter)}"
        if node.get("units", None):
            set_tree_ids(node["units"], node["id"])


def get_tree_node(nodes: list[dict], query_id: str) -> dict | None:
    """Return the first node matching the `query_id`, if it exists

    Args:
        nodes (list[dict]): The deeply nested json list
        query_id (str): The id previously set by `set_tree_ids()`

    Returns:
        dict | None: The first node matching the query_id or None
    """
    for node in nodes:
        if node["id"] == query_id:
            return node
        if units := node.get("units", None):
            if match := get_tree_node(units, query_id):
                return match


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
