class Table:
    def __init__(self, data):
        self._columns = list(data)
        self._data = {}

        for col, rows in data.items():
            self._data[col] = rows.copy()

        self._types = {}

        for cols in self._columns:
            self._types[cols] = str

    def _resolve_column(self, column):
        if isinstance(column, int):
            return self._columns[column]
        else:
            return column

    def get_values(self, column):
        column = self._resolve_column(column)
        return self._data[column].copy()

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

