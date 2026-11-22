import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"

table1 = tb.load_csv(test_data)
table2 = tb.load_csv(test_data)

table = tb.Table(
    columns=["id", "name", "score"],
    data=[
        [1, "Alice", 10],
        [None, "Bob", 20],
        [3, "Charlie", None],
        [4, "David", 0]
    ],
    types={"id": int, "name": str, "score": int}
)

selected = table.get_rows_by_index(3, copy_table=True)
print(selected._data[0] is table._data[2])
