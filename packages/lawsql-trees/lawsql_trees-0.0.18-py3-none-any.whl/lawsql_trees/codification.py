import itertools
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator, NoReturn, Optional

from dotenv import find_dotenv, load_dotenv
from lawsql_utils.trees import data_tree_walker
from lawsql_utils.trees.identities import set_tree_ids

from .fts import get_rows_with_key_from_dict
from .utils import format_citations, get_citation

load_dotenv(find_dotenv())


@dataclass
class CodificationItem:
    """Each validated yaml file is parsed to create a `CodificationItem`.

    Upon loading the the file, the following properties validate:
    1. `complete_data`
    2. `get_units`
    3. `statutes_in_sync`
    4. `get_histories`

    If validation does not raise any exceptions, pull history data from `get_histories`.

    Aside from generic metadata, this dataclass contains two complex keys:
    1. `units`: A list of nested `unit` dicts - each `unit` may contain a `history`.
    2. `histories`: A list of `history` dicts - each `history` indicates a `Statute` or a `Decision`.

    Each `unit` of object's `units` represent an element of the `base` Statute as modified by the `requisites`.
    """

    path_to_code_yaml: Path

    def __post_init__(self):
        from lawsql_utils.general import format_full_date

        self.data: dict = self.fetch_complete_data_from_file
        self.publication_date: date = format_full_date(self.data["date"])
        self.sync = self.statutes_in_sync
        self.units: list[dict] = self.data["units"]
        self.version = str(self.data["version"])
        self.emails: list[str] = self.data["emails"]
        self.title = self.data["title"]
        self.description = self.data["description"]
        self.base = self.data["base"]
        self.histories: list[dict] = self.get_histories

    @property
    def fetch_complete_data_from_file(self) -> NoReturn | dict:
        """If there are any missing keys, raise error."""
        from lawsql_tree_unit import format_units
        from lawsql_utils.files import load_yaml_from_path

        raw_data = load_yaml_from_path(self.path_to_code_yaml)
        for key in [
            "title",
            "description",
            "version",
            "emails",
            "date",
            "version",
            "base",
            "requisites",
            "units",
        ]:
            if key not in raw_data:
                raise Exception(f"Missing {key}")
        format_units(raw_data["units"])  # fixes item, caption, content
        format_citations(raw_data["units"])  # adjusts the canonical citations
        set_tree_ids(raw_data["units"])  # adds id to each node

        return raw_data

    @property
    def decision_fts_row_ids(self) -> Iterator[int]:
        """Each of the units may contain query strings under a `queries` key. Collect all of these from all the units to get the rowids of the Decisions table."""
        source = {"units": self.units}
        rows = get_rows_with_key_from_dict(source, "queries")
        for data in rows:
            yield data["rowid"]

    @property
    def citations_from_histories(self) -> set[str] | NoReturn:
        """Get all strings of Decision Citations found in the "citation" key in the nested dictionary"""
        return set(data_tree_walker(self.data, "citation"))

    @property
    def citations_in_db(self) -> list[str] | NoReturn:
        """If no error is raised, either there are no citations (an empty list) in the codification or all citations have a corresponding match (a list of dicts)"""
        matched_citations = []
        if texts := self.citations_from_histories:
            citation_list = list(texts)  # convert set to list
            for text in citation_list:
                if citation_found := get_citation(text):
                    matched_citations.append(citation_found["raw"].canonical)
                else:
                    err_msg = (
                        f"Could not find citation in the database: {text=}"
                    )
                    raise Exception(err_msg)
        return matched_citations

    @property
    def statutes_from_histories(self) -> set[str] | NoReturn:
        """Get all strings of Statutes found in the "statute" key in the nested dictionary"""
        if not (blocks := set(data_tree_walker(self.data, "statute"))):
            raise Exception(f"No statute blocks found; see {blocks=}")
        return blocks

    @property
    def requisites_sans_base(self) -> set[str]:
        """Get set of texts representing statute serial names without the base statute for the codification."""
        return set(self.data["requisites"])

    @property
    def statutes_in_requisites(self) -> set[str]:
        """Get set of texts representing statute serial names with the base statute for the codification."""
        return set(self.data["requisites"] + [self.data["base"]])

    @property
    def statutes_in_sync(self) -> bool | NoReturn:
        """Indicates that Statutes found in history blocks match stated requisites."""
        if err := self.statutes_from_histories - self.statutes_in_requisites:
            raise Exception(f"In body not in requisites: {str(err)=}")
        if err := self.statutes_in_requisites - self.statutes_from_histories:
            raise Exception(f"In requisites not in body: {str(err)=}")
        return True

    @property
    def get_history_lists(self) -> list[list[dict]] | NoReturn:
        """Each unit may have its history; each history is a list of blocks"""
        if not (l := list(data_tree_walker(self.data, "history"))):
            raise Exception(f"No history blocks; see {l=}")
        return l

    @property
    def get_histories(self) -> list[dict] | NoReturn:
        """Get histories by flattening list (chain)"""
        return list(itertools.chain(*self.get_history_lists))


def get_matching_yaml_filenames(
    folder: Path, q: Optional[str] = None
) -> Iterator[Path]:
    """With folder given, return generator of yaml files; if a specific string `q` is supplied, only match proper files."""
    return folder.glob(f"{q}*.yaml" if q else "*.yaml")


def get_author_codification_folder(
    author: str = "mv3",
) -> NoReturn | Path:
    """Implies preset `PATH_TO_LAWSQL` with subfolder `codifications`"""
    l = os.getenv("PATH_TO_LAWSQL").split("/") + ["codifications", author]
    folder = Path.home().joinpath(*l)
    if not folder.exists():
        raise Exception(f"{folder=} could not be found.")
    return folder


def get_codifications(author: str = "mv3", q: str = None):
    """Gets all codifications within a specific author `folder` (default is `mv3`), matching the query `q` of a preset base `PATH_TO_LAWSQL` with subfolder `codifications`"""
    folder = get_author_codification_folder(author)
    return get_matching_yaml_filenames(folder, q)
