def print_table(self):
    columns = list(self._data[0].keys())
    n_rows = len(self._data)

    str_headers = [str(c) for c in columns]
    str_rows = [[str(row[c]) for c in columns] for row in self._data]

    numeric = [
        all(isinstance(row[c], (int, float)) and not isinstance(row[c], bool) for row in self._data)
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