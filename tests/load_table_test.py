import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"

print("1 таблица")
table1 = tb.load_csv(test_data)

print(table1.get_data(), sep="\n")
print("\n Несколько таблиц")
tables = tb.load_csv(test_data, dota_data)
print("1 таблица")
print(tables[0].get_data())
print("============================================")
print("2 таблица")
print(tables[1].get_data())

print("============================================")
print("\nбез пути к таблице")

a = tb.load_csv()
print(a)
print("===========================================\n")
b = tb.load_csv(null_data)



