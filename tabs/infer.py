from datetime import datetime
from functools import lru_cache
import re


INT_PATTERN = re.compile(r"^\s*-?\d+\s*$")
FLOAT_PATTERN = re.compile(r"^\s*-?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*$")
DATETIME_PRECHECK = re.compile(
    r"^\s*\d{1,2}([.-])\d{1,2}\1(\d{2}|\d{4})( \d{1,2}:\d{2}(:\d{2}(\.\d{1,6})?)?)?\s*$"
)
DATETIME_FORMATS = [
    "%d-%m-%Y %H:%M:%S.%f",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m-%Y %H:%M",
    "%d-%m-%Y",
    "%d-%m-%y %H:%M:%S",
    "%d-%m-%y %H:%M",
    "%d-%m-%y",

    "%d.%m.%Y %H:%M:%S.%f",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H:%M",
    "%d.%m.%Y",
    "%d.%m.%y %H:%M:%S",
    "%d.%m.%y %H:%M",
    "%d.%m.%y",
]
bool_map = {"true": True, "false": False}


@lru_cache(maxsize=4096)
def _is_datetime(value):
    if not DATETIME_PRECHECK.match(value):
        return False

    normalized = value.strip().replace(".", "-")

    for fmt in DATETIME_FORMATS:
        try:
            datetime.strptime(normalized, fmt)
            return True

        except ValueError:
            continue

    return False

def _is_float(value):
    return bool(FLOAT_PATTERN.match(value))

def _is_int(value):
    return bool(INT_PATTERN.match(value))

def _get_cell_type(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return datetime

    if isinstance(value, bool):
        return bool

    if isinstance(value, int):
        return int

    if isinstance(value, float):
        return float

    if not isinstance(value, str):
        raise TypeError(f"Недопустимый тип данных: {type(value)}")

    if _is_datetime(value):
        return datetime

    if _is_int(value):
        return int

    if _is_float(value):
        return float

    if value.lower() in bool_map:
        return bool

    return str

def _merge_types(types):
    if any(_type in types for _type in (str, datetime, bool)):
        raise TypeError(f"Несочетаемые типы данных: {types}")

    if float in types:
        return float

    if int in types:
        return int

    raise ValueError(f"в {types} содержится недопустимый тип данных")


def infer_column_types(columns: list, rows: list) -> dict:
    if not columns:
        raise ValueError("Отсутствуют названия столбцов")

    types = {column: str for column in columns}

    n_cols = len(columns)
    for idx, row in enumerate(rows, start=1):
        if len(row) != n_cols:
            raise ValueError(
                f"в {idx} строке {len(row)} полей вместо {n_cols}"
            )

    for column_index in range(n_cols):
        column_types = set()
        for row in rows:
            cell_type = _get_cell_type(row[column_index])
            if cell_type is not None:
                column_types.add(cell_type)

        if len(column_types) == 1:
            types[columns[column_index]] = next(iter(column_types))
        elif len(column_types) > 1:
            types[columns[column_index]] = _merge_types(column_types)

    _is_datetime.cache_clear()
    return types