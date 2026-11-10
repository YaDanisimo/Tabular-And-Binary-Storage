from .table import Table
import csv


def load_table(*paths, header=None, encoding="utf-8", delimiter=",", newline=""):
    tables = []
    paths_len = len(paths)

    if paths_len == 0:
        return None

    if header is None or isinstance(header, int):
        header = [header] * paths_len
    elif isinstance(header, list):
        if len(header) != paths_len:
            raise ValueError("ДОДЕЛАТЬ")
    else:
        raise ValueError("ДОДЕЛАТЬ")


    for idx in range(paths_len):
        dct = {"age": 0, "number"}
        with open(paths[idx], mode="r", encoding=encoding, newline=newline) as file:
            csv_table = csv.reader(file, delimiter=delimiter)

            i = -1
            for row in csv_table:
                i += 1

                if i == header[idx]:
                    columns = row
                    continue

                rows.append(row)

            if header[idx] is None and rows:
                columns = [i for i in range(len(rows[0]))]

        tables.append(Table(columns, rows))

    return tables[0] if len(tables) == 1 else tables


def save_table(table, name, path, max_rows)