import itertools
import re
from typing import Iterator

from bs4 import BeautifulSoup
from markdown2 import markdown
from treeish import fetch_values_from_key

from .utils import DB_FILE

sql = """--sql
    select
        d.rowid,
        d.source,
        d.pk,
        d.date_prom date_promulgated,
        snippet(
            fts_result.Decisions_fts, --the table for full-text search
            3, --the index found in the Decisions table
            '', --no need to mark before the match
            '', --no need to mark after the match
            '...',
            128
        ) search_result
    from Decisions_fts fts_result
    join Decisions d on d.rowid = fts_result.rowid
    where Decisions_fts match ?
    order by date_promulgated desc;
"""


def convert_to_snippet(text: str):

    footnote_pattern = re.compile(
        r"""
        \[
        \^
        \d+
        \]:?""",
        re.X,
    )
    repl = footnote_pattern.sub("", text)
    mded = markdown(repl)
    html = BeautifulSoup(mded, "html5lib")
    return html.get_text(separator=" ", strip=True)


def get_rows_with_key_from_dict(data: dict, key: str) -> Iterator[dict]:
    def extract_queries(data: dict, key: str):
        yield from fetch_values_from_key(data, key)

    queries = itertools.chain(*extract_queries(data, key))
    joined_text = '" OR "'.join(queries)
    rows = DB_FILE.execute(
        sql, (f'"{joined_text}"',)
    )  # note extra double quote
    for row in rows:
        yield {
            "rowid": row[0],
            "source": row[1],
            "pk": row[2],
            "date": row[3],
            "snippet": convert_to_snippet(row[4]),
        }
