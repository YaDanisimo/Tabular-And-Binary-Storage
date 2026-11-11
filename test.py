from copy import deepcopy

columns = {}
data = [
    {"name": "Alex", "age": 23, "City": "Moscow"},
    {"name": "Pidr", "age": 18, "City": "Kiev"},
    {"name": "Misha", "age": 3, "City": "Minsk"},
    {"name": "Petya", "age": 13, "City": "NewYork"}
]

def get_rows_by_number(table, start, stop, copy_table=True):
    if not copy_table:
        return table[start:stop]

    return deepcopy(table[start:stop])

table_new = get_rows_by_number(table, 0, 3, copy_table=True)

print(table_new)