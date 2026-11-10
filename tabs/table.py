class Table:
    def __init__(self, columns, rows):

        if len(set(columns)) != len(columns):
            raise ValueError('Ожидались уникальные столбцы!')

        for row in rows:

            if len(row) != len(columns):
                raise ValueError('Некорректная запись!')

        self._columns = tuple(columns)
        self._rows = rows
        self._types = [str] * len(columns)

    def get_values(self, column_name):
        column = column_name
        if not column.isdigit(): # если название столбца != индексу
            column = name_to_index[column] # берём индекс столбца по названию

        column_index = self._columns.index(column)
        values = []

        for row in self._rows:
            values.append(row[column_index])
        return values

    def set_values(self, column, values):
        if len(self._rows) != len(values):
            raise ValueError('Не совпадают строки и значения!')

        column_index = self._columns.index(column)

        for i, row in enumerate(self._rows):
            row[column_index] = values[i]

    def get_column_types(self):
        columns_types = {}
        for column, column_type in zip(self._columns, self._types):
            columns_types[column] = column_type
        return columns_types

    def set_column_types(self, column_types):
        converted_columns = {}
#  Готовим новые значения
        for column, column_type in column_types.items():
            column_index = self._columns.index(column)
            converted_values = []

            for row in self._rows:
                converted_values.append(column_type(row[column_index]))
            converted_columns[column_index] = (column_type, converted_values)
#  Изменяем таблицу
        for column_index, (column_type, values) in converted_columns.items():

            for i, row in enumerate(self._rows):

                row[column_index] = values[i]

            self._types[column_index] = column_type

