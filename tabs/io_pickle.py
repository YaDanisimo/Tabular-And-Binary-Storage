from .table import Table
import pickle

def _get_data(path):
    with open(path, mode='rb') as file:
        data = pickle.load(file)

    return data

def load_table(*paths):
    tables = []

    if not paths:
        return None

    for path in paths:
        table = Table(_get_data(path))
        tables.append(table)

    return tables[0] if len(tables) == 1 else tables


def save_table(table: Table, path, max_rows=None):
    data = table.get_data()

    with open(path, mode='wb') as file:
        pickle.dump(data, file)

