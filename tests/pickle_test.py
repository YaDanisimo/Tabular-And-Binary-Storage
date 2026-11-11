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
table2.print_table()



