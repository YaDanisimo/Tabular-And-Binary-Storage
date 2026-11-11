
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
        column = self._resolve_column(column)
        if len(values) != len(self._data[column]):
            raise ValueError('Количество новых значений не равно количеству строк!')
        else:
            self._data[column][:] = values

    def get_column_types(self):
        return self._types.copy()

    def set_column_types(self, column_types):
        converted_columns = {}

        for col, col_type in column_types.items():
            col = self._resolve_column(col)
            values = self._data[col]
            converted_values = []

            for value in values:
                converted_values.append(col_type(value))
            converted_columns[col] = (col_type, converted_values)

        for col, col_converted in converted_columns.items():
            col_type, values = col_converted
            self._data[col][:] = values
            self._types[col] = col_type

    def get_data(self):
        return self._data