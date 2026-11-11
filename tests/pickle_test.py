import tabs as tb
from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"
test_0 = ROOT / "tests" / "saved_test_files" / "test_0.csv"


table1 = tb.load_csv(test_data, header=True)

tb.save_pickle(table1, "test.pkl")
table2 = tb.load_pickle("test.pkl")
#table2.print_table()

dct = {"age": [3, 14, 18, 21, 35]}

dct1 = {"age": [3, 14, 18]}


columns = ["name", "age"]
rows = [
    ["Alex", 23],
    ["Pidr", 18],
    ["Misha", 3]
]

table = [
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

table_new[0]["name"] = "Max"
print(table)

