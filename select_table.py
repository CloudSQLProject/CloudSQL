import json
import os

import PrettyTable

from staticString import StaticString


def select(table_name, static_string):
    table_file = f'./{table_name}.json'
    if not os.path.exists(table_file):
        print(static_string.TABLE_NOT_EXIST)
    else:
        with open(table_file) as f:
            response = json.load(f)
    table = PrettyTable()
    table.filed_name = ['id', 'name', 'age']
    for row in response:
        for column in row.values():
            table.add_row(column)
    print(table)



staticString = StaticString()
select('student', staticString)
