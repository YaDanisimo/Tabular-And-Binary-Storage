import re

INT_PATTERN = re.compile(r"^\s*[+-]?\d+\s*$")
FLOAT_PATTERN = re.compile(r"^\s*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*$")
BOOL_MAP = {"true": True, "false": False}


def _is_integer(text: str) -> bool:
    return bool(INT_PATTERN.match(text))


def _is_floating(text: str) -> bool:
    return bool(FLOAT_PATTERN.match(text))


def _detect_cell_type(cell_value):
    if cell_value is None:
        return type(None)
    if isinstance(cell_value, bool):
        return bool
    if isinstance(cell_value, int):
        return int
    if isinstance(cell_value, float):
        return float
    if isinstance(cell_value, str):
        stripped_text = cell_value
        if stripped_text.lower() in BOOL_MAP:
            return bool
        if _is_integer(stripped_text):
            return int
        if _is_floating(stripped_text):
            return float
        return str
    return object


def _merge_column_types(detected_type, new_type):
    if detected_type is None:
        return new_type
    if new_type is None:
        return detected_type

    if detected_type is object or new_type is object:
        return object
    if detected_type is type(None) or new_type is type(None):
        return object

    if detected_type is new_type:
        return detected_type

    if {detected_type, new_type} == {int, float}:
        return float

    return object


def _cast_value(raw_value, target_type):
    if raw_value is None:
        return None

    if target_type is object:
        return raw_value if isinstance(raw_value, str) else raw_value

    if target_type is bool:
        if isinstance(raw_value, bool):
            return raw_value
        if isinstance(raw_value, str):
            return BOOL_MAP[raw_value.lower()]
        return bool(raw_value)

    if target_type is str:
        return str(raw_value)

    # Для int и float
    if isinstance(raw_value, str):
        raw_value = raw_value

    return target_type(raw_value)


def infer_types(data):
    if not data:
        return {}

    headers = list(data[0].keys())
    column_types = {}

    for column_name in headers:
        current_type = None
        for record in data:
            cell_type = _detect_cell_type(record[column_name])
            current_type = _merge_column_types(current_type, cell_type)

        column_types[column_name] = current_type if current_type is not type(None) else object

    for record in data:
        for column_name in headers:
            record[column_name] = _cast_value(record[column_name], column_types[column_name])

    return column_types


# ----------------- ТЕСТ -----------------
if __name__ == "__main__":
    dataset = [
        {"id": "1", "price": "1.5", "is_active": "True", "name": "hello", "comment": None},
        {"id": "2", "price": "2", "is_active": "False", "name": "world", "comment": None},
        {"id": "-3", "price": "3.14", "is_active": "true", "name": "!", "comment": None},
        {"id": "4", "price": None, "is_active": "false", "name": "test", "comment": "ok"},
    ]

    print(infer_types(dataset))
