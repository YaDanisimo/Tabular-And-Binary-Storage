import tabs as tb


table1 = tb.load_csv("C:/code/myBeautifulProjects/Tabular-And-Binary-Storage/datasets/test_data.csv")
print(table1._data)

tb.save_csv(table1, max_rows=20)