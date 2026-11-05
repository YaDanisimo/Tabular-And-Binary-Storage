## Архитектура проекта
- `__init__.py` — публичный API пакета (реэкспорт).
- `table.py` — класс `Table, get/set значений и типов и тд
- `io_csv.py` — загрузка/сохранение CSV.
- `io_pickle.py` — загрузка/сохранение pickle.
- `text.py` — сохранение таблицы в текстовый файл.
- `ops.py` — арифметика, сравнения, `filter_rows`.
- `combine.py` — `concat`, `split`, `merge_tables`.
- `infer.py` — автоопределение типов столбцов.
- `errors.py` — исключения пакета.