from prettytable import PrettyTable

def display_table(data, columns, title="Table View"):
    if data:
        table = PrettyTable()
        table.field_names = columns
        for row in data:
            table.add_row(row)

        for i, column in enumerate(columns):
            if isinstance(data[0][i], (int, float)):
                table.align[column] = "r"  # Right align numbers
            else:
                table.align[column] = "l"  # Left align strings

        print(f"\n{title}")
        print(table)
    else:
        print("No records found.")
