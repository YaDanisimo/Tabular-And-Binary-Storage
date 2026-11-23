from .table import Table
from .autotype import autotype
from pathlib import Path
import csv


def _get_table_data(path, headers, delimiter, encoding, newline):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")

    with open(path, mode='r', encoding=encoding, newline=newline) as file:
        rows = list(csv.reader(file, delimiter=delimiter))

    if not rows:
        return None, []

    n_cols = len(rows[0])

    if isinstance(headers, (list, tuple)):
        if len(headers) != n_cols:
            raise ValueError(
                f"{path}: длина header ({len(headers)}) "
                f"не совпадает с числом столбцов в файле ({n_cols})"
            )

        if not all(isinstance(name, str) for name in headers):
            raise TypeError(
                f"{path}: все имена столбцов в headers должны быть str"
            )

        column_names = list(headers)
        data_rows = rows

    elif headers is True:
        column_names = list(rows[0])
        data_rows = rows[1:]

    elif headers is None:
        column_names = [str(name) for name in range(n_cols)]
        data_rows = rows

    else:
        raise ValueError(
            f"header должен быть только True, None или list/tuple[str]\n"
            f"получено {type(headers).__name__}"
        )

    offset = 2 if headers is True else 1
    data = []
    for idx, row in enumerate(data_rows, start=offset):
        if len(row) != n_cols:
            raise ValueError(
                f"{path}, строка {idx}: {len(row)} полей вместо {n_cols}"
            )

        data.append([value if value != "" else None for value in row])

    return column_names, data


def load_table(*paths, headers=True, encoding: str ="utf-8", delimiter: str =",",
               newline: str = "", auto_types: bool = True):
    if not paths:
        raise ValueError("Не передан ни один путь к файлу")

    if len(delimiter) != 1:
        raise ValueError(f"delimiter должен быть одним символом, получено {delimiter}")

    common_columns = None
    all_data = []

    for path in paths:
        columns, data = _get_table_data(
            path, headers=headers, delimiter=delimiter,
            encoding=encoding, newline=newline,
        )

        if columns is None:
            raise ValueError(f"Файл пуст: {path}")

        if common_columns is None:
            common_columns = columns

        elif columns != common_columns:
            raise ValueError(
                f"Структура столбцов в {path} не совпадает с первым файлом:\n"
                f"    ожидалось: {common_columns}\n"
                f"    получено:  {columns}"
            )

        all_data.extend(data)

    if not all_data:
        raise ValueError(
            f"Таблица пуста (0 строк данных). Файлы: {paths}"
        )

    table = Table(common_columns, all_data)
    autotype(table)

    return table


def _save_csv(rows, path, encoding, headers, delimiter, newline):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode="w", encoding=encoding, newline=newline) as file:
        writer = csv.writer(file, delimiter=delimiter)

        if headers is not None:
            writer.writerow(headers)
        writer.writerows(rows)


def save_table(table: Table, name: str = "test", path: Path | str ="saved_test_files/", max_rows=None,
               save_headers=True, delimiter: str = ",", encoding="utf-8", newline=""):
    if not isinstance(table, Table):
        raise TypeError(f"Ожидалась Table, получено {type(table)}")

    if len(delimiter) != 1:
        raise ValueError(f"delimiter должен быть одним символом, получено {delimiter}")

    headers = table.columns if save_headers else None
    _, data, _ = table.unzip

    base = Path(path) / name

    if max_rows is None:
        current_path = base.with_suffix(".csv")
        _save_csv(data, current_path, encoding, headers, delimiter, newline)

    elif isinstance(max_rows, int) and not isinstance(max_rows, bool) and max_rows > 0:
        left_border = 0
        right_border = max_rows
        data_size = len(data)

        file_prefix = 0
        while left_border < data_size:
            chunked_rows = data[left_border:right_border]

            current_path = base.with_name(f"{base.name}_{file_prefix}.csv")

            _save_csv(chunked_rows, current_path, encoding, headers, delimiter, newline)

            left_border += max_rows
            right_border = min(right_border + max_rows, data_size)
            file_prefix += 1

    else:
        raise ValueError(f"max_rows должен быть положительным int или None, получено {max_rows}")
