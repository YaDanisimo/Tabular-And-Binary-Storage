from copy import deepcopy


class Table:
    def __init__(self, data, types):
        self._columns = list(data[0])
        self._data = data


        self._types = types

        for col in self._columns:
            self._types[col] = str


    def _resolve_column(self, column):
        if isinstance(column, int):
            return self._columns[column]
        else:
            return column


    def get_values(self, column):
        column = self._resolve_column(column)
        values = []

        for row in self._data:
            values.append(row[column])

        return values


    def set_values(self, column, values):
        column = self._resolve_column(column)

        if len(values) != len(self._data):
            raise ValueError('Количество новых значений не равно количеству строк!')
        for row, value in zip(self._data, values):
                row[column] = value


    def get_column_types(self):
        return self._types.copy()


    def set_column_types(self, column_types):
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


    def get_data(self):
        return self._data


    def set_value(self, column, value):
        column = self._resolve_column(column)

        if len(self._data) != 1:
            raise ValueError('Ожидался одна строка!')

        self._data[0][column] = value


    def get_value(self, column):
        column = self._resolve_column(column)

        if len(self._data) != 1:
            raise ValueError('Ожидался одна строка!')

        return self._data[0][column]


    def get_rows_by_number(self, start, stop=None, copy_table=False):
        if stop is None:
            stop = start + 1

        selected = self._data[start:stop]

        if copy_table:
            selected = deepcopy(selected)

        return Table(selected)


    def get_rows_by_index(self, *values, copy_table=False):
        index_column = self._columns[0]
        rows = []

        for row in self._data:
            if row[index_column] in values:
                rows.append(row)

        if copy_table:
            rows = deepcopy(rows)

        return Table(rows)


    def print_table(self):
        columns = self._columns
        n_rows = len(self._data)

        if not columns:
            print("Таблица не содержит столбцов.")
            return

        headers = [str(col) for col in columns]
        rows = [
            [str(row[col]) for col in columns]
            for row in self._data
        ]

        numeric = [
            n_rows > 0 and all(
                isinstance(row[col], (int, float))
                and not isinstance(row[col], bool)
                for row in self._data
            )
            for col in columns
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