import tabs as tb

print("1 таблица")
table1 = tb.load_csv("tabs/test_data.csv", header=0)
print(table1._columns)
print(*table1._rows[:5], sep="\n")
print("\n Несколько таблиц")
tables = tb.load_csv("tabs/test_data.csv", "tabs/dota_data.csv", header=[2, None])
print("1 таблица")
print(tables[0]._columns)
print(*tables[0]._rows[:5], sep="\n")
print("============================================")
print("2 таблица")
print(tables[1]._columns)
print(*tables[1]._rows[:5], sep="\n")
print("============================================")
print("\nбез пути к таблице")

a = tb.load_csv()
print(a)
print("===========================================\n")
b = tb.load_csv("tabs/null.csv")
print(b._columns)
print(b._rows, sep="\n")



data = {
    "col1": [...],
    "col2": [...],
    "col3": [...],
    "col4": [...],
}

table = Table(data)
table.get_value(column="column_name")
table.get_value(column=0) # <- {0: "name", 1: "age", 2: "size"}

