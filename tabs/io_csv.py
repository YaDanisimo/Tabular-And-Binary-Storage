from .table import Table
import csv

# преобразует csv в словарь
def _get_dictionary(path, header, delimiter, encoding, newline):
    with open(path, mode='r', encoding=encoding, newline=newline) as file:
        reader = csv.reader(file, delimiter=delimiter)
        rows = [row for row in reader if any(cell.strip() for cell in row)]

    if not rows:
        return {}

    len_rows = len(rows[0])
    if isinstance(header, (list, tuple)):
        if len(header) != len_rows:
            raise ValueError("не совпадает количечетсво столбцов. Доделать")
        for name in header:
            if not isinstance(name, str):
                raise TypeError(f"недопустимый тип данных для столбца: {type(name)}")
        column_names = list(header)
    elif header is True:
        column_names = rows[0]
        rows = rows[1:]
    elif header is None:
        column_names = list(range(len_rows))
    else:
        raise ValueError("header must be list or tuple or None or True")

    data = []
    for row in rows:
        data.append({})
        for idx, value in enumerate(row):
            data[-1][column_names[idx]] = value

    return data

# создаёт таблицы из словарей, созданных в get_dictionary
def load_table(*paths, header=True, encoding="utf-8", delimiter=",", newline=""):
    if not paths:
        return None

    tables = []

    for path in paths:
        data = _get_dictionary(
            path, header=header, delimiter=delimiter,
            encoding=encoding, newline=newline
        )

        tables.append(Table(data))

    return tables[0] if len(tables) == 1 else tables


def _save_csv(rows, path, encoding, save_names, delimiter, newline):
    with open(path, mode="w", encoding=encoding, newline=newline) as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), delimiter=delimiter)
        if save_names:
            writer.writeheader()
        writer.writerows(rows)


def save_table(table: Table, path="saved_test_files/test.csv", max_rows=None, save_names=True, delimiter=",", encoding="utf-8", newline=""):
    data = table.get_data()

    if path[-4:] == ".csv":
        path = path[:-4]

    if max_rows is None:
        _save_csv(data, path, encoding, save_names, delimiter, newline)
    elif isinstance(max_rows, int) and max_rows > 0:
        left_border = 0
        right_border = max_rows
        data_size = len(data)
        file_prefix = 0
        while left_border < data_size:
            chunked_rows = data[left_border:right_border]
            _save_csv(chunked_rows, path + f"_{file_prefix}.csv", encoding, save_names, delimiter, newline)

            left_border += max_rows
            right_border = min(right_border + max_rows, data_size)
            file_prefix += 1
    else:
        raise ValueError("max_rows говно. ДОДЕЛАТЬ")
