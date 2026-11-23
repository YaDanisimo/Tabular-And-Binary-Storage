from copy import deepcopy
from datetime import datetime
from .autotype import autotype, _cast_column

class Table:
    """
    _columns - список столбцов
    _data - список строк
    _types - словарь {столбец: тип}
    """

    def __init__(self, columns: list[str], data: list[list], types: dict = None): # нужен ли types
        self._columns = list(columns)
        self._data = list(data)

        if types is None:
            self._types = {col: str for col in self._columns}
        else:
            self._types = dict(types)

    """ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ"""

    def _resolve_column(self, column):
        if isinstance(column, int):
            return self._columns[column]
        else:
            return column

    def _column_index(self, column):
        """Возвращает индекс столбца по имени или индексу апхахппх"""
        name = self._resolve_column(column)
        return self._columns.index(name)


    """ДЛЯ ОТЛАДКИ / ФИЧИ"""

    @property
    def columns(self):
        return list(self._columns)

    @property
    def types(self):
        return dict(self._types) # так создаётся копия

    @property
    def data(self):
        return deepcopy(self._data)

    @property
    def unzip(self): # не создаёт копии
        return self._columns, self._data, self._types

    def __len__(self):
        return len(self._data)

    """ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ""" # get функции

    def get_values(self, column):
        column = self._column_index(column)
        values = []

        for row in self._data:
            values.append(row[column])

        return values

    def get_value(self, column):

        if len(self._data) != 1:
            raise ValueError('Ожидалась одна строка!')

        value =  self.get_values(column)

        return value[0]

    def get_rows_by_number(self, start, stop=None, copy_table=False):
        if stop is None:
            stop = start + 1

        selected = self._data[start:stop]

        if copy_table:
            selected = deepcopy(selected)

        return Table(self._columns, selected, types=self.types)


    def get_rows_by_index(self, *values, copy_table=False):
        index_column = 0
        rows = []

        for row in self._data:
            if row[index_column] in values:
                rows.append(row)

        if copy_table:
            rows = deepcopy(rows)

        if len(rows) == 0:
            raise ValueError("Пустая таблица!")

        return Table(self._columns, rows, self._types)



    """ДЛЯ ИЗМЕНЕНИЯ ДАННЫХ""" # set функции


    def set_values(self, column, values): # будем ли вызывать ошибку если
                                          # в столбце с типом int будет заменять всё на строки
                                          # или лучше вызывать после этого что-то из autotype.py
        column = self._resolve_column(column)

        if len(values) != len(self._data):
            raise ValueError('Количество новых значений не равно количеству строк!')
        for row, value in zip(self._data, values):
                row[column] = value

    def set_column_types(self, column_types): # используй _cast_column из autotype.py
        converted_columns = {}

        for col, col_type in column_types.items():
            col = self._resolve_column(col)
            values = self.get_values(col)
            converted_values = []

            for value in values:
                converted_values.append(col_type(value))
            converted_columns[col] = (col_type, converted_values)

        for col, col_converted in converted_columns.items():
            col_type, values = col_converted
            self.set_values(col, values)
            self._types[col] = col_type



    def set_value(self, column, value):
        column = self._resolve_column(column)

        if len(self._data) != 1:
            raise ValueError('Ожидался одна строка!')

        self._data[0][column] = value


    """ВЫВОД ТАБЛИЦЫ"""

    def print_table(self):
        columns = self._columns  # list
        n_rows = len(self._data)  # list[list]
        n_cols = len(columns)

        if not columns:
            print("Таблица не содержит столбцов.")
            return

        headers = [str(col) for col in columns]

        # _data — список списков, поэтому приводим значения по индексу
        rows = [
            [str(value) for value in row]
            for row in self._data
        ]

        # проверка "числовости" столбца по индексу i
        numeric = [
            n_rows > 0 and all(
                isinstance(row[i], (int, float))
                and not isinstance(row[i], bool)
                for row in self._data
            )
            for i in range(n_cols)
        ]

        widths = []
        for i, header in enumerate(headers):
            width = len(header)
            for row in rows:
                width = max(width, len(row[i]))
            widths.append(width)

        index_width = max(1, len(str(n_rows - 1)))
        sep = "  "

        header_line = sep.join(
            header.rjust(width) if is_numeric else header.ljust(width)
            for header, width, is_numeric in zip(headers, widths, numeric)
        )

        print(" " * index_width + sep + header_line.rstrip())

        for i, row in enumerate(rows):
            formatted_row = sep.join(
                value.rjust(width) if is_numeric else value.ljust(width)
                for value, width, is_numeric in zip(row, widths, numeric)
            )
            print(str(i).rjust(index_width) + sep + formatted_row.rstrip())

    def __repr__(self):
        return f"Table(columns={self._columns}, rows={len(self._data)}"

