import json
import os

table_keys = {}
table_columns = {}

def create_table(table_name, *columns):
    table_file = f'./{table_name}.json'
    if not os.path.exists(table_file):
        with open(table_file, 'w') as file:
            initial_data = []
            json.dump(initial_data, file)
        columns = [column.strip(',') for col_group in columns for column in col_group.split(',')]
        print(f'Table {table_name} created successfully with columns: {columns}')
        global table_columns
        global table_keys
        table_columns[table_name] = columns
        primary_key = input("Enter the primary key for the table: ")
        if primary_key not in columns:
            print("Primary key does not exist in the table columns")
            os.remove(table_file)
            return
        table_keys[table_name] = primary_key
        #print(table_columns)
        #print(table_keys)
    else:
        print(f'Table {table_name} already exists')

    with open('shared_data.py', 'w') as f:
        f.write(f"table_columns = {table_columns}\n")
        f.write(f"table_keys = {table_keys}\n")

def add_record(table_name, values):
    table_file = f'./{table_name}.json'
    if os.path.exists(table_file):
        with open(table_file, 'r') as file:
            data = json.load(file)
        columns = table_columns.get(table_name, [])
        if not columns:
            print(f'Columns for table {table_name} not found')
            return
        if len(values) != len(columns):
            print(f'Error: Number of values does not match the number of columns for table {table_name}')
            return
        record = {column: value for column, value in zip(columns, values)}
        if any(all(record.get(key) == value for key, value in row.items()) for row in data):
            print('Record already exists')
        else:
            data.append(record)
            with open(table_file, 'w') as file:
                json.dump(data, file, indent=4)
            print('Record added successfully')
    else:
        print(f'Table {table_name} does not exist')

def create_table_main():
    while True:
        user_input = input("Enter command: ")
        parts = user_input.split()
        if len(parts) < 4:
            print('Invalid command')
            continue
        command = parts[0]
        table_name = parts[2]
        if command == 'create' and len(parts) > 3 and parts[3] == 'columns':
            columns = [column.strip(',') for column in parts[4:]]
            create_table(table_name, *columns)
        elif command == 'insert' and len(parts) > 3 and parts[3] == 'values':
            values = [value.strip('(),') for value in parts[4:]]
            add_record(table_name, values)
        else:
            print('Invalid command')

if __name__ == '__main__':
    create_table_main()