import json
import os
import re
import field
import table_format
import shutil
import pickle
from shared_data import table_columns,table_keys
from collections import defaultdict
#create table table_name(id int key not_null, name varchar(20) not_key not_null); 对应field字段每一个属性


def create_table(table_name, columns):
    column_names = [column.name for column in columns]
    table_columns[table_name] = column_names
    table_keys[table_name] = columns[0].name

    table_directory = f"dir/user_default/db0/{table_name}"
    if os.path.exists(table_directory):
        print(f"Table {table_name} already exists")
    else:
        test_table = table_format.Table(table_name, columns)
        test_table.save()



def find_id_with_primary_key(datas, primary_key_value):
    for data in datas:
        if data.get('primary_key') == 'key':
            return data.get('name')


primary_keys = set()

def load_existing_data(table_file):
    global primary_keys
    if os.path.exists(table_file):
        with open(table_file, 'r') as f:
            existing_data = json.load(f)
            for record in existing_data:
                primary_key_value = record.get('id')  # 假设主键的字段名为 'id'
                if primary_key_value:
                    primary_keys.add(primary_key_value)
    else:
        print(f'File {table_file} does not exist')




def add_record(table_name, values):
    directory = "dir/user_default/db0"  # 目标目录
    table_directory = os.path.join(directory, table_name)
    table_file = table_directory + f'/{table_name}.json'
    table_struct = table_directory + f'/{table_name}_struct.json'
    load_existing_data(table_file)
    if os.path.exists(table_file):
        with open(table_struct, 'r') as file:
            datas = json.load(file)
        elements = values.split(',')
        if len(elements) != len(datas):
            print(f'Error: Number of values does not match the number of columns for table {table_name}')
            return
        else:
            primary_key_value = None
            for i in range(len(datas)):
                if datas[i]['primary_key'] == 'key':
                    primary_key_value = elements[i]
                    if primary_key_value in primary_keys:
                        print('Record with the same primary key already exists')
                        return
                    else:
                        primary_keys.add(primary_key_value)
            if primary_key_value is None:
                print('No primary key provided')
                return
            record = {}
            for i in range(len(datas)):
                record[datas[i]['name']] = elements[i]
            with open(table_file, 'r') as f:
                existing_data = json.load(f)
            existing_data.append(record)

            with open(table_file, 'w') as f:
                json.dump(existing_data, f, indent=4)  # 将数据写入 JSON 文件中，格式化缩进为4个空格

            print('Record added successfully')
    else:
        print(f'Table {table_name} does not exist')



#insert table table_name values(1,fucking)
def drop_table(table_name):
    directory = "dir/user_default/db0"  # 目标目录
    table_directory = os.path.join(directory, table_name)

    if os.path.exists(table_directory):
        try:
            # 关闭文件句柄并删除文件/目录
            shutil.rmtree(table_directory)  # 使用递归删除整个目录
            print('Table deleted successfully')
        except OSError as e:
            print(f"删除文件{table_name}时出错: {e}")
    else:
        print(f'Table {table_name} does not exist')


def rename_table(old_table_name, new_table_name):
    directory = "dir/user_default/db0"  # 目标目录
    old_table_directory = os.path.join(directory, old_table_name)
    new_table_directory = os.path.join(directory, new_table_name)
    # 检查原表是否存在
    if os.path.exists(old_table_directory):
        try:
            # 重命名目录
            os.rename(old_table_directory, new_table_directory)
            # 遍历新目录下的所有文件
            for root, dirs, files in os.walk(new_table_directory):
                for file in files:
                    # 判断文件名是否以旧表名前缀开头
                    if file.startswith(f"{old_table_name}"):
                        # 构造新文件名
                        new_file_name = file.replace(f"{old_table_name}", f"{new_table_name}")
                        # 构造文件的完整路径
                        old_file_path = os.path.join(root, file)
                        new_file_path = os.path.join(root, new_file_name)
                        # 进行重命名操作
                        os.rename(old_file_path, new_file_path)
            print(f"Table '{old_table_name}' renamed to '{new_table_name}' successfully")
        except OSError as e:
            print(f"重命名表时出错: {e.strerror}")
    else:
        print(f"Table '{old_table_name}' does not exist. Rename operation aborted.")

def delete_column(table_name, column_name):
    # 构建表格文件路径
    table_file = f'./{table_name}.json'
    # 如果表格文件存在
    if os.path.exists(table_file):
        # 从表格文件中加载数据
        with open(table_file, 'r') as file:
            data = json.load(file)
        # 获取表格的列信息
        columns = table_columns.get(table_name, [])
        # 如果表格的列信息不存在
        if not columns:
            print(f'Columns for table {table_name} not found')
            return
        # 如果指定的列名不在表格的列信息中
        if column_name not in columns:
            print(f'Column {column_name} does not exist in table {table_name}')
            return
        # 遍历表格数据，删除指定列名的数据
        for record in data:
            record.pop(column_name, None)
        # 保存更新后的数据回表格文件中
        with open(table_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f'Column {column_name} deleted successfully from table {table_name}')
    # 如果表格文件不存在
    else:
        print(f'Table {table_name} does not exist')

def create_table_main():
    #理想中的sql语句

    global fields, table_name
    while True:
        user_input = input("Enter command: ")
        # 定义要匹配的字符串
        sql_statement = user_input
        # 使用正则表达式匹配最外层括号内的内容
        parts = user_input.split()


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
            print("over")

        #chu li insert yu ju  ji ben ge shi wei


        elif command == 'insert' and len(parts) > 3:
            # 定义匹配的正则表达式模式
            pattern = r'insert table (\w+) values\(([^)]+)\)'

            # 使用正则表达式进行匹配
            match = re.match(pattern, sql_statement)

            if match:
                table_name = match.group(1)
                values = match.group(2)
                print(f"Table name: {table_name}")
                print(f"Values: {values}")
            else:
                print("illegal insert")

            add_record(table_name, values)



        elif command == 'drop' and len(parts) == 3 and parts[1] == 'table':
            drop_table(table_name)

        # drop table your_table_name
        elif command == 'drop':
            match = re.search(r'drop\s+table\s+[\'"]?(\w+)[\'"]?', sql_statement)
            if match:
                table_name = match.group(1)  # 获取表名
                # 调用删除表的函数，传递表名
                drop_table(table_name)
            else:
                print("Invalid drop table command")

        elif command == 'delete' and len(parts) > 3 and parts[3] == 'columns':
            columns = parts[4:]
            delete_column(table_name, *columns)  # 调用删除记录的函数
        elif command == 'rename':
            match = re.search(r'rename\s+table\s+(\w+)\s+(\w+)', sql_statement, re.IGNORECASE)
            if match:
                old_table_name = match.group(1)  # 获取原表名
                new_table_name = match.group(2)  # 获取新表名
                # 调用重命名表的函数，传递原表名和新表名
                rename_table(old_table_name, new_table_name)
            else:
                print("Invalid rename table command")
        else:
            print('Invalid command')