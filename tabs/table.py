from copy import deepcopy
from datetime import datetime
from .autotype import autotype, _cast_column, _cast_value

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


    def get_value(self, column=0):

        if len(self._data) != 1:
            raise ValueError('Ожидалась одна строка!')

        value =  self.get_values(column)

        return value[0]

    def get_values(self, column=0):
        column = self._column_index(column)
        values = []

        for row in self._data:
            values.append(row[column])

        return values

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

    def get_column_types(self, by_number=True):
        if not by_number:
            return self.types

        types = {}

        for column_name, type_ in self.types.items():
            column = self._column_index(column_name)
            types[column] = type_

        return types

    """ДЛЯ ИЗМЕНЕНИЯ ДАННЫХ""" # set функции


    def set_value(self, value, column=0):  # Изменяет значение согласно ожидаемому и изменяет _data
        if len(self._data) != 1:
            raise ValueError('Ожидалась одна строка!')

        column = self._column_index(column)
        expected_type = self._types[self._columns[column]]

        if value is not None and type(value) is not expected_type:
            value = _cast_value(value, type(value), expected_type)

        self._data[0][column] = value

    def set_values(self, values, column=0): # преобразуем новые значения под ожидаемый тип столбца
        column = self._column_index(column)
        expected_type = self._types[self._columns[column]]
        converted_values = []

        if len(values) != len(self._data):
            raise ValueError('Количество новых значений не равно количеству строк!')

        for value in values:
            if type(value) is not expected_type and value is not None:
                value = _cast_value(value, type(value), expected_type)
            converted_values.append(value)

        for new_value, old_row in zip(converted_values, self._data):
            old_row[column] = new_value

    def set_column_types(self, types_dict, by_number=True): # выполняет преобразование на глубокой копии, а затем заменяет данные и обновляет _types только у той таблицы, на которой его вызвали
        data = deepcopy(self._data)
        types = deepcopy(self._types)

        for column, new_type in types_dict.items():
            TypeErrors = False
            if by_number and type(column) is not int:
                TypeErrors = True
            elif not by_number and type(column) is not str:
                TypeErrors = True
            if TypeErrors:
                raise TypeError('Некорректный тип ключа!')

            column_index = self._column_index(column)

            column_name = self._columns[column_index]
            cur_type = self._types[column_name]

            _cast_column(data, column_index, cur_type, new_type)
            types[column_name] = new_type

        self._data = data
        self._types = types

    """ПОДДЕРЖКА ОПЕРАЦИЙ СРАВНЕНИЯ""" # САНЯ СЮДА ПИШЕШЬ

    """ПОДДЕРЖКА АРИФМЕТИЧЕСКИХ ОПЕРАЦИЙ"""
    def __add__(self, other):
        if other.idi_naxyi

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __rsub__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __rtruediv__(self, other):
        pass

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
        return f"Table(columns={self._columns}, rows={len(self._data)})"

