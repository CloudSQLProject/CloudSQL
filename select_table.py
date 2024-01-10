import json
import os

from prettytable import PrettyTable

from staticString import StaticString


def select(table_name, static_string):
    table_file = f'./{table_name}.json'
    if not os.path.exists(table_file):
        print(static_string.TABLE_NOT_EXIST)
    else:
        with open(table_file) as f:
            response = json.load(f)
    table = PrettyTable()
    fieldName = ['id', 'name', 'age']
    table.field_names = (fieldName)
    for row in response:
        values = list(row.values())
        table.add_row(values)
    print(table)


staticString = StaticString()
select('student', staticString)
