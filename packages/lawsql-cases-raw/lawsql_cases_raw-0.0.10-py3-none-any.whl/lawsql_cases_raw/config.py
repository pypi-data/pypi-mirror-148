import re
from collections import namedtuple

MAX_LENGTH_IDX = 100
MAX_RAW_PONENTE = 35
MAX_CASE_TITLE = 1000
MAX_FALLO = 20000
PER_CURIAM_PATTERN = re.compile(r"per\s+curiam", re.I)

MatchedRows = namedtuple("MatchedRows", ["counts", "rows"])
