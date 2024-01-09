import json
import os

def create_table(table_name, *columns):
    table_file = f'./{table_name}.json'
    if not os.path.exists(table_file):
        with open(table_file, 'w') as file:
            initial_data = []
            json.dump(initial_data, file)
        print(f'Table {table_name} created successfully with columns: {columns}')
    else:
        print(f'Table {table_name} already exists')

def add_record(table_name, record):
    table_file = f'./{table_name}.json'
    if os.path.exists(table_file):
        with open(table_file, 'r') as file:
            data = json.load(file)
        data.append(record)
        with open(table_file, 'w') as file:
            json.dump(data, file, indent=4)
        print('Record added successfully')
    else:
        print(f'Table {table_name} does not exist')

def main():
    while True:
        user_input = input("Enter command: ")
        parts = user_input.split(',')
        command = parts[0].split()[0]
        table_name = parts[0].split()[-1]

        if command == 'create':
            columns = [column.strip() for column in parts[1:]]
            create_table(table_name, *columns)
        elif command == 'insert':
            record = {parts[i]: parts[i+1] for i in range(1, len(parts), 2)}
            add_record(table_name, record)
        else:
            print('Invalid command')

if __name__ == '__main__':
    main()
