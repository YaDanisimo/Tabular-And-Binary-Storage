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


def _save_pickle(path, data):
    with open(path, mode='wb') as file:
        pickle.dump(data, file)


def save_table(table: Table, path, max_rows=None):
    data = table.get_data()
    if path[-4:] == ".pkl":
        path = path[:-4]

    if max_rows is None:
        _save_pickle(path, data)

    elif isinstance(max_rows, int) and max_rows > 0:
        data_size = len(data)
        left_border = 0
        right_border = max_rows

        prefix = 0
        while left_border < data_size:
            chunked_data = data[left_border:right_border]
            _save_pickle(path + f"_{prefix}.pkl", chunked_data)

            prefix += 1
            left_border += max_rows
            right_border = min(right_border + max_rows, data_size)