from typing import Optional

from sqlite_utils import Database

from .config import MatchedRows


def match_report(pattern: str, text: str) -> Optional[MatchedRows]:
    from citation_report.__main__ import get_report_formats

    from .utils import decisions_tbl

    try:
        result = next(get_report_formats(text))
        if pattern in result.lower():
            counts = decisions_tbl.count_where(f"{pattern} = ?", (result,))
            rows = decisions_tbl.rows_where(f"{pattern} = ?", (result,))
            return MatchedRows(counts=counts, rows=rows)
    except:
        ...
    return None


def rows_from_report_text(text: str) -> Optional[MatchedRows]:
    return match_report("phil", text) or match_report("scra", text)
