import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"
path = ROOT / "datasets" / "minecraft.csv"

table = tb.load_csv(path)

# 1. GET
assert len(table) == 20
assert table.get_values() == [row[0] for row in table.data]
assert table.get_column_types()[3] is int
assert table.get_column_types(False)["blocks_mined"] is int

row = table.get_rows_by_number(1, copy_table=True)
assert row.get_value() == table.get_values()[1]

index = table.get_values()[0]
assert table.get_rows_by_index(index).data[0] == table.data[0]

# 2. SET VALUE
original = table.data

row.set_value("500", "blocks_mined")
assert row.get_value("blocks_mined") == 500
assert table.data == original

# 3. SET VALUES
table.set_values(["500"] * len(table), "blocks_mined")
assert table.get_values("blocks_mined") == [500] * len(table)

# 4. SET COLUMN TYPES
table.set_column_types({"blocks_mined": float}, by_number=False)

assert table.types["blocks_mined"] is float
assert all(type(v) is float for v in table.get_values("blocks_mined"))

# 5. ПРОВЕРКА НЕУДАЧНОГО ПРЕОБРАЗОВАНИЯ
original = table.data
original_types = table.types

try:
    table.set_column_types(
        {"session_status": int},
        by_number=False
    )
except (ValueError, TypeError):
    pass
else:
    raise AssertionError("Ожидалась ошибка преобразования!")

assert table.data == original
assert table.types == original_types

print("Все основные проверки Table пройдены!")



