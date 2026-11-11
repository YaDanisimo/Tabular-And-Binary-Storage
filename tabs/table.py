
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

    def set_value(self, column, value):
        column = self._resolve_column(column)

        if len(self._data[column]) != 1:
            raise ValueError('Ожидался одна строка!')

        else:
            self._data[column] = [value]

    def get_value(self, column):
            column = self._resolve_column(column)

            if len(self._data[column]) != 1:
                raise ValueError('Ожидался одна строка!')

            else:
                return self._data[column][0]



    def print_table(self):
        columns = list(self._data.keys())
        n_rows = len(self._data[columns[0]])

        str_headers = [str(c) for c in columns]
        str_rows = [[str(self._data[c][i]) for c in columns] for i in range(n_rows)]

        numeric = [
            all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in self._data[c])
            for c in columns
        ]

        widths = [
            max([len(h)] + [len(r[i]) for r in str_rows])
            for i, h in enumerate(str_headers)
        ]

        idx_width = len(str(n_rows - 1))
        sep = "  "

        print(" " * idx_width + sep + sep.join(
            (h.rjust(w) if nr else h.ljust(w))
            for h, w, nr in zip(str_headers, widths, numeric)
        ).rstrip())

        for i, row in enumerate(str_rows):
            print((str(i).rjust(idx_width) + sep + sep.join(
                (c.rjust(w) if nr else c.ljust(w))
                for c, w, nr in zip(row, widths, numeric)
            )).rstrip())