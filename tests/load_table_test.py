import tabs as tb

print("1 таблица")
table1 = tb.load_csv("tabs/test_data.csv")

print(table1.data, sep="\n")
print("\n Несколько таблиц")
tables = tb.load_csv("tabs/test_data.csv", "tabs/dota_data.csv")
print("1 таблица")
print(tables[0].data)
print("============================================")
print("2 таблица")
print(tables[1].data)

print("============================================")
print("\nбез пути к таблице")

a = tb.load_csv()
print(a)
print("===========================================\n")
b = tb.load_csv("tabs/null.csv")
print(b.data)


