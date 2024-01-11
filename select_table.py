import json
import os
#from prettytable import PrettyTable

def select(table_name, static_string):
    table_file = f'./{table_name}.json'
    if not os.path.exists(table_file):
        print(static_string.TABLE_NOT_EXIST)
    else:
        with open(table_file) as f:
            response = json.load(f)

    if len(response) == 0:
        print("Table is empty")
        return

    keys = response[0].keys()
    max_lengths = [len(str(key)) for key in keys]
    rows = []

    for row in response:
        values = list(row.values())
        rows.append(values)
        max_lengths = [max(max_lengths[i], len(str(values[i]))) for i in range(len(values))]

    header = "|".join([f"{key:<{max_lengths[i]}}" for i, key in enumerate(keys)])
    separator = "+".join(["-" * (max_lengths[i] + 2) for i in range(len(keys))])
    #print(separator)
    print(header)
    #print(separator)

    for row in rows:
        formatted_row = "|".join([f"{value:<{max_lengths[i]}}" for i, value in enumerate(row)])
        print(formatted_row)
        #print(separator)
class StaticString:
    TABLE_NOT_EXIST = "Table does not exist"

staticString = StaticString()
select('student', staticString)
