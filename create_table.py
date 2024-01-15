import json
import os
import re
import field
import table_format

table_keys = {}
table_columns = {}

def create_table(table_name, columns:field.Field):
    #columns[0].name
    print(columns[0].name)#参数可以传递 类型是field
    print(vars(columns[0]))
    test_table= table_format.Table(table_name,columns)
    test_table.save()

    # table_file = f'./{table_name}.json'
    # if not os.path.exists(table_file):
    #     with open(table_file, 'w') as file:
    #         initial_data = []
    #         json.dump(initial_data, file)
    #     columns = [column.strip(',') for col_group in columns for column in col_group.split(',')]
    #     print(f'Table {table_name} created successfully with columns: {columns}')
    #     global table_columns
    #     global table_keys
    #     table_columns[table_name] = columns
    #     primary_key = input("Enter the primary key for the table: ")
    #     if primary_key not in columns:
    #         print("Primary key does not exist in the table columns")
    #         os.remove(table_file)
    #         return
    #     table_keys[table_name] = primary_key
    #     #print(table_columns)
    #     #print(table_keys)
    # else:
    #     print(f'Table {table_name} already exists')
    #
    # with open('shared_data.py', 'w') as f:
    #     f.write(f"table_columns = {table_columns}\n")
    #     f.write(f"table_keys = {table_keys}\n")

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
    #理想中的sql语句
    #create table table_name(id int key not_null, name varchar(20) not_key not_null); 对应field字段每一个属性
    while True:
        user_input = input("Enter command: ")
        # 定义要匹配的字符串
        sql_statement = user_input
        # 使用正则表达式匹配最外层括号内的内容
        parts = user_input.split()
        # if len(parts) < 4:
        #     print('Invalid command')
        #     continue
        command = parts[0]#在以上的sql中只有part[0]是有效的识别命令符
        print(command)
        # 使用正则表达式匹配整个create table语句
        if command == 'create' :
            match = re.search(r'create table \w+\((.*)\)', sql_statement)  # 使用正则表达式匹配最外层括号内的内容
            if match:
                content_inside_outer_parentheses = match.group(1)  # 获取最外层括号内的内容
                fields = [x.strip() for x in content_inside_outer_parentheses.split(',')]  # 以逗号为分隔符分割内容成列表
                print("Columns:", fields)
            else:
                print("sql语句格式错误")
            #columns = [column.strip(',') for column in parts[4:]]
            match = re.search(r'create table (\w+)\(', sql_statement)  # 使用正则表达式匹配整个create table语句，并提取表名部分
            if match:
                table_name = match.group(1)  # 获取表名
                print("Table Name:", table_name)
            #已知表名和各属性之后,创建sql语句对应的文件
            struct_table_list=[]
            for column in fields:
                struct=column.split()
                print(struct)
                print(column)
                struct_table= field.Field(struct[0], struct[1], struct[2], struct[3])
                struct_table_list.append(struct_table)

            print(struct_table_list)
            create_table(table_name, struct_table_list)
       # # elif command == 'insert' and len(parts) > 3 and parts[3] == 'values':
       #      values = [value.strip('(),') for value in parts[4:]]
       #      add_record(table_name, values)
        else:
            print('Invalid command')

if __name__ == '__main__':
    create_table_main()