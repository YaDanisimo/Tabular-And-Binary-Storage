import tabs

tablica = tabs.load_csv("tabs/test_data.csv", header=0)

print(tablica._columns)


print(tablica.get_values("age"))
print(tablica.get_values(2))

