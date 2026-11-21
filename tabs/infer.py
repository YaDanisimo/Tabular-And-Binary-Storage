from datetime import datetime
import re


INT_PATTERN = re.compile(r"^\s*[+-]?\d+\s*$")
FLOAT_PATTERN = re.compile(r"^\s*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*$")
bool_map = {"true": True, "false": False}

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

    if _is_int(value):
        return int

    if _is_float(value):
        return float

    if value.lower() in bool_map:
        return bool

    return str

def _merge_types(types):
    if str in types or datetime in types:
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

    return types