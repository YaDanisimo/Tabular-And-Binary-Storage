import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"

table = tb.load_csv(test_data)
table = tb.load_csv(test_data)

selected = table.get_rows_by_index("2", "5", "10")
selected.print_table()
print(selected.get_values("id"))
print(selected.get_values("name"))
table = tb.load_csv(test_data)

view = table.get_rows_by_index("2")

print("До:", table.get_values("city")[1])

view.set_value("city", "TEST_CITY")

print("После:", table.get_values("city")[1])
table = tb.load_csv(test_data)

copied = table.get_rows_by_index("2", copy_table=True)

copied.set_value("city", "TEST_CITY")

print("Копия:", copied.get_value("city"))
print("Оригинал:", table.get_values("city")[1])

