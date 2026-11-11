import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"
test_0 = ROOT / "tests" / "saved_test_files" / "test_0.csv"

print(test_data)
table1 = tb.load_csv(test_data, header=True)
tb.save_csv(table1, max_rows=10)

table_short = tb.load_csv(test_0, header=True)
table_short.print_table()