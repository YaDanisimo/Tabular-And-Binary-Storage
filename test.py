from copy import deepcopy

table = [
    {"name": "Alex", "age": 23, "City": "Moscow"},
    {"name": "Pidr", "age": 18, "City": "Kiev"},
    {"name": "Misha", "age": 3, "City": "Minsk"},
    {"name": "Petya", "age": 13, "City": "NewYork"}
]



table_new = get_rows_by_number(table, 0, 3, copy_table=True)

print(table_new)