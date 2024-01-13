import json
import os
import static_string
from shared_data import table_keys,table_columns


class StaticString:
    TABLE_NOT_EXIST = "Table does not exist"
staticString = StaticString()


def get_user_input(user_input):
    parts = user_input.split(' ')
    if len(parts) < 4 or parts[0].lower() != 'select' or parts[2].lower() != 'from':
        print("Invalid command")
        return None,None,None
    else:
        aim = parts[1].split(',')
        table = parts[3]
        where_condition = None
        if len(parts)>4 and parts[4].lower() == 'where':
            where_condition = ' '.join(parts[5:])
        return aim,table,where_condition

def draw_table(data, keys, max_lengths):
    header = "|".join([f"{key:<{max_lengths[i]}}" for i, key in enumerate(keys)])
    separator = "+".join(["-" * (max_lengths[i] + 2) for i in range(len(keys))])
    #print(separator)
    print(header)
    #print(separator)
    for row in data:
        formatted_row = "|".join([f"{value:<{max_lengths[i]}}" for i, value in enumerate(row)])
        print(formatted_row)
        #print(separator)


def select_all(table_name,static_string):
    table_file = f'./{table_name}.json'
    if not os.path.exists(table_file):
        print(static_string.TABLE_NOT_EXIST)
        return []
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
    draw_table(rows, keys, max_lengths)


def select_column(table_name, aim, where_condition):
    if table_name in table_keys:
        primary_key = table_keys[table_name]
        if primary_key not in aim:
            aim.insert(0, primary_key)
    else:
        print(f"Error: Table {table_name} not found in table_keys")
        return

    table_file = f'./{table_name}.json'
    if not os.path.exists(table_file):
        print("Table does not exist")
        return []

    with open(table_file) as f:
        response = json.load(f)
        if len(response) == 0:
            print("Table is empty")
            return []

        result = []
        if where_condition:
            condition_key, condition_value = where_condition.split('==')
            for row in response:
                if condition_key in row and str(row[condition_key]) == condition_value:
                    entry = {}
                    for key in aim:
                        if key in row:
                            entry[key] = row[key]
                    result.append(entry)
        else:
            for row in response:
                entry = {}
                for key in aim:
                    if key in row:
                        entry[key] = row[key]
                result.append(entry)

        keys = result[0].keys() if result else []
        max_lengths = [len(str(key)) for key in keys]
        rows = []
        for row in result:
            values = list(row.values())
            rows.append(values)
            max_lengths = [max(max_lengths[i], len(str(values[i])) if values[i] else 0) for i in range(len(values))]
        draw_table(rows, keys, max_lengths)





def main():
    while True:
        user_input = input("Enter Command: ")
        aim,table,where_condition= get_user_input(user_input)
        #print(aim,table,where_condition)
        if aim == ['*']:
            select_all(table,static_string)
        else:
            select_column(table,aim,where_condition)


if __name__ == "__main__":
    main()