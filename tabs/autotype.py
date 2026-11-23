from datetime import datetime
from functools import lru_cache
import re


INT_PATTERN = re.compile(r"^\s*-?\d+\s*$")
FLOAT_PATTERN = re.compile(r"^\s*-?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*$")
DATETIME_PRECHECK = re.compile(
    r"^\s*(\d{4}|\d{1,2})([.-])\d{1,2}\2(\d{2}|\d{4})"
    r"( \d{1,2}:\d{2}(:\d{2}(\.\d{1,6})?)?)?\s*$"
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

    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
]
BOOL_MAP = {"true": True, "false": False}


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

    if value.lower() in BOOL_MAP:
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


def _parse_datetime(value: str) -> datetime:
    if not DATETIME_PRECHECK.match(value):
        raise ValueError(f"Невозможно привести '{value}' к datetime")

    normalized = value.strip().replace(".", "-")
    for fmt in DATETIME_FORMATS:
        try:
            return datetime.strptime(normalized, fmt)
        except ValueError:
            continue

    raise ValueError(f"Невозможно привести '{value}' к datetime")


def _cast_value(value, cur_type, new_type):
    if value is None:
        return None

    if new_type is str:
        if cur_type is bool:
            return "true" if value else "false"

        if cur_type is datetime:
            return value.isoformat()

        return str(value)

    if new_type is datetime:
        if cur_type is str:
            if _is_datetime(value):
                return _parse_datetime(value)

        raise ValueError(f"Невозможно привести '{value}' к datetime")

    if new_type is bool:
        if cur_type is str:
            if value.lower() in BOOL_MAP:
                return BOOL_MAP[value.lower()]

        elif cur_type is int:
            if value in (0, 1):
                return value == 1

        elif cur_type is float:
            if value in (0.0, 1.0):
                return value == 1.0

        raise ValueError(f"Невозможно привести '{value}' к bool")


    if new_type is int:
        if cur_type is str:
            if _is_int(value):
                return int(value)

        elif cur_type in (float, bool): # Вопрос. Значения или округляются, или вызывается ошибка
            return int(value)

        raise ValueError(f"Невозможно привести {value} к int")

    if new_type is float:
        if cur_type is str:
            if _is_float(value):
                return float(value)

        elif cur_type is int: # bool подкласс int
            return float(value)

        raise ValueError(f"Невозможно привести {value} к float")

    raise TypeError(f"Приведение из {cur_type} в {new_type} не поддерживается")


def _cast_column(data, column_index: int, cur_type, new_type):
    """
    Приводит значения столбца в указанный тип

    data - ссылка на список строк таблицы
    column_index - индекс столбца
    cur_type - текущий тип значений в столбце
    new_type - тип значений, в которой нужно привести значения
    """
    if not data:
        return

    n_cols = len(data[0])
    if column_index < 0 or column_index >= n_cols:
        raise IndexError(f"Индекс столбца {column_index} вне диапазона [0, {n_cols - 1}]")

    if new_type not in (int, float, bool, str, datetime):
        raise TypeError(f"Неподдерживаемый тип данных: {new_type}")

    if cur_type is new_type:
        return

    new_values = []
    for idx, row in enumerate(data, start=1):
        value = row[column_index]
        new_values.append(_cast_value(value, cur_type, new_type))

    for row, new_value in zip(data, new_values):
        row[column_index] = new_value


def autotype(table):
    """
    Автоматически определяет тип каждого столбца.
    Переводит значения столбца в его тип.
    """
    columns, data, cur_types = table.unzip
    if not columns:
        raise ValueError("Отсутствуют названия столбцов")

    new_types = dict(cur_types)

    n_cols = len(columns)
    for idx, row in enumerate(data, start=1):
        if len(row) != n_cols:
            raise ValueError(
                f"в {idx} строке {len(row)} полей вместо {n_cols}"
            )

    for column_index in range(n_cols):
        column_types = set()
        for row in data:
            cell_type = _get_cell_type(row[column_index])
            if cell_type is not None:
                column_types.add(cell_type)

        col_name = columns[column_index]
        if len(column_types) == 1:
            new_types[col_name] = next(iter(column_types))
        elif len(column_types) > 1:
            new_types[col_name] = _merge_types(column_types)

        _cast_column(data, column_index, cur_types[col_name], new_types[col_name])
        cur_types[col_name] = new_types[col_name]

    _is_datetime.cache_clear()