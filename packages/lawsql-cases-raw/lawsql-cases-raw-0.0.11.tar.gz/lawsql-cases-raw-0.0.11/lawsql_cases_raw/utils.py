import datetime as dt
import os
from pathlib import Path

from dateutil.parser import parse
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
from sqlite_utils import Database

home = Path().home()
decisions_path = home.joinpath(os.getenv("DECISIONS"))
db_path = home.joinpath(os.getenv("PATH_TO_DB"))
db = Database(db_path, use_counts_table=True)
decisions_tbl = db["Decisions"]


def parse_date_if_exists(text: str = None) -> dt.date | None:
    """If the variable contains text with more than 5 characters, parse possible date."""
    if not text:
        return None
    elif text and len(text) < 5:
        return None
    elif not (parsed := parse(text)):
        return None
    return parsed.date()
