import json
import os
import re
from shared_data import table_keys,table_columns

conditions = []

def parse_where_conditions(where_condition):
    conditions = []
    sub_conditions = re.split(r'\b(?: or )\b', where_condition)
    for sub_condition in sub_conditions:
        and_conditions = re.split(r'\b(?: and )\b', sub_condition)
        conditions.append(and_conditions)
    return conditions

def apply_condition(row, condition):
    match = re.match(r'(\w+)\s*([<>=]+)\s*(\w+)', condition)
    if match:
        condition_key, condition_op, condition_value = match.groups()
        condition_key = condition_key.strip()
        condition_value = condition_value.strip()
        if condition_op == '=':
            return row.get(condition_key) == condition_value
        elif condition_op == '<':
            return row.get(condition_key) < condition_value
        elif condition_op == '>':
            return row.get(condition_key) > condition_value
    return False


def get_user_input(user_input):
    global conditions
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
            conditions = parse_where_conditions(where_condition)
            print(conditions)
        return aim,table,conditions

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


def select_all(table_name,where_condition):
    return select_column(table_name,table_columns[table_name],where_condition)


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
            for row in response:
                condition_met = False
                for sub_conditions in where_condition:
                    sub_condition_met = any(apply_condition(row, condition) for condition in sub_conditions)
                    if sub_condition_met:
                        condition_met = True
                        break
                if condition_met:
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
    global conditions
    conditions = []
    while True:
        conditions = []
        user_input = input("Enter Command: ")
        aim,table,where_condition= get_user_input(user_input)
        #print(aim,table,where_condition)
        if aim == ['*']:
            select_all(table,where_condition)
        else:
            select_column(table,aim,where_condition)


if __name__ == "__main__":
    main()