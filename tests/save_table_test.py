import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"
test_0 = ROOT / "tests" / "saved_test_files" / "test_0.csv"


table1 = tb.load_csv(test_data, headers=True)
tb.save_csv(table1, max_rows=10, save_headers=True)

table_short = tb.load_csv(test_0, headers=True)
table_short.print_table()

print("\nFIRST NICE\n")

table1 = tb.load_csv(test_data, headers=True)
tb.save_csv(table1, max_rows=10, save_headers=False)

table_short = tb.load_csv(test_0, headers=True)
table_short.print_table()

print("\nSECOND NICE\n")

#
table1 = tb.load_csv(test_data, headers=True)
tb.save_csv(table1, max_rows=25, save_headers=False)

print("\nTHIRD NICE\n")


table_short = tb.load_csv(test_0, headers=None)
table_short.print_table()

print("\nFOURTH NICE\n")
