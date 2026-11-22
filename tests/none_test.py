import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"
mine_data = ROOT / "datasets" / "minecraft.csv"

table1 = tb.load_csv(mine_data)
table1.print_table()
print(table1.data)
print(table1.get_column_types())
