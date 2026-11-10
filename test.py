import tabs

tablica = tabs.load_csv("tabs/test_data.csv", header=None)

print(tablica._columns)
print(*tablica._rows, sep="\n")

print(tablica.get_values("age"))
print(tablica.get_values(2))

