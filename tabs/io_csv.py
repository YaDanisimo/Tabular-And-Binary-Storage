from .table import Table
import csv

# преобразует csv в словарь
def get_dictionary(path, header, delimiter, encoding, newline):
    with open(path, mode='r', encoding=encoding, newline=newline) as file:
        reader = csv.reader(file, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        return {}

    if isinstance(header, (list, tuple)):
        column_names = list(header)
    elif header is True:
        column_names = rows[0]
        rows = rows[1:]
    elif header is None:
        column_names = list(range(len(rows[0])))
    else:
        raise ValueError("header must be list or tuple or None or True")

    data = {col: [] for col in column_names}
    for row in rows:
        for idx, value in enumerate(row):
            print(idx, value, column_names[idx])
            data[column_names[idx]].append(value)

    return data

# создаёт таблицы из словарей, созданных в get_dictionary
def load_table(*paths, header=True, encoding="utf-8", delimiter=",", newline=""):
    if not paths:
        return None

    tables = []

    for path in paths:
        data = get_dictionary(
            path, header=header, delimiter=delimiter,
            encoding=encoding, newline=newline
        )

        tables.append(Table(data))

    return tables[0] if len(tables) == 1 else tables
