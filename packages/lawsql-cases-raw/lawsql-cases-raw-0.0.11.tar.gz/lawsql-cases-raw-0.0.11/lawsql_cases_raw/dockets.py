from typing import Optional

from citation_docket import is_docket

from .config import MatchedRows


def rows_from_docket(
    validated_docket_category: str,
    validated_docket_idx: str,
    formatted_date_string: str = None,
) -> MatchedRows:
    """The `cat` and `idx` in the query string are fixed table fields;
    The `cat_param` and `idx_param` are sourced from values of the defined dict of `is_docket`
    The query string is constructed with validated parameter variables

    Args:
        validated_docket_category (str): Value is sourced `is_docket`; created by `get_docket_category`
        validated_docket_idx (str): Value is sourced `is_docket`; validated by `valid_idx`
        formatted_date_string (str, optional): Value is sourced `is_docket`; created by `get_date`. Defaults to None.

    Returns:
        MatchedRows: [description]
    """
    from .utils import decisions_tbl

    queries: list[str] = ["cat = :cat_param", "idx like :idx_param"]
    params: dict[str, str] = {
        "cat_param": validated_docket_category,
        "idx_param": f"%{validated_docket_idx}%",
    }
    if formatted_date_string:
        queries.append("date(date_prom) = date(:date_param)")
        params |= {"date_param": formatted_date_string}

    return MatchedRows(
        decisions_tbl.count_where(" and ".join(queries), params),
        decisions_tbl.rows_where(" and ".join(queries), params),
    )


def rows_fom_docket_text(raw: str) -> Optional[MatchedRows]:
    return rows_from_docket(*d.values()) if (d := is_docket(raw)) else None
