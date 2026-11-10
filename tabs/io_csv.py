from .table import Table
import csv

def load_table(path: str, header=None, encoding="utf-8", delimiter=",", newline=""):
    columns = None
    rows = []
    with open(path, mode="r", encoding=encoding, newline=newline) as file:
        csv_table = csv.reader(file, delimiter=delimiter)

        i = -1
        for row in csv_table:
            i += 1

            if i == header:
                columns = row
                continue

            rows.append(row)

        if header is None and rows:
            columns = [i for i in range(len(rows[0]))]

    return Table(columns, rows)
