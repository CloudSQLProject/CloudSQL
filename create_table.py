import json
import os
import re
import field
import table_format


def create_table(table_name, columns:field.Field):
    #columns[0].name
    print(columns[0].name)#参数可以传递 类型是field
    print(vars(columns[0]))
    directory = "dir/user_default/db0"  # 目标目录
    table_directory = os.path.join(directory, table_name)
    if  os.path.exists(table_directory):
        print(f'Table {table_name} already exists')
    else:
        test_table= table_format.Table(table_name,columns)
        test_table.save()



def add_record(table_name, values):

    directory = "dir/user_default/db0"  # 目标目录d
    table_directory = os.path.join(directory, table_name)
    table_file=table_directory+f'/{table_name}.json'
    #table_file = f'{table_file}.json'
    table_struct = table_directory + f'/{table_name}_struct.json'
    print(table_file+"第一阶段测试")
    print(table_struct)
    #表名存在就开始找字典里字段以jason插入数据
    if os.path.exists(table_file):
        with open(table_struct, 'r') as file:
            datas = json.load(file)
        print(datas)
        name=[]
        for data in datas:
            name.append(data['name'])
            print(data)
        #columns = table_columns.get(table_name, [])
        print(name)
        #处理values 将其变为jason格式
        ele=values.split(',')
        print(ele)


        if len(values) != len(datas):
            print(f'Error: Number of values does not match the number of columns for table {table_name}')
            return

      #判断是否由主键冲突,也就是找到字段里主键和扫描文件里主键元素集,插入的不能冲突


            print('Record already exists')
        else:
            data.append(record)
            with open(table_file, 'w') as file:
                json.dump(data, file, indent=4)
            print('Record added successfully')
    else:
        print(f'Table {table_name} does not exist')


def drop_table(table_name):
    table_file = f'./{table_name}.json'
    if os.path.exists(table_file):
        try:
            os.remove(table_file)  # 删除table对应json文件
            print('Table deleted successfully')
        except OSError as e:
            print(f"删除文件{table_name}时出错: {e.strerror}")


def rename_table(table_name_old, table_name_new):
    table_file_old = f'./{table_name_old}.json'
    table_file_new = f'./{table_name_new}.json'
    if os.path.exists(table_file_old):
        if not os.path.exists(table_file_new):
            os.rename(table_file_old, table_file_new)
            print(f'Table {table_name_new} renamed successfully')
        else:
            print(f"The new name {table_name_new} exists")
    else:
        print(f"Table {table_name_old} not exists")


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
    #create table table_name(id int key not_null, name varchar(20) not_key not_null); 对应field字段每一个属性
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
        #insert table table_name values(1,"fucking")

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
        elif command == 'delete' and len(parts) > 3 and parts[3] == 'columns':
            columns = parts[4:]
            delete_column(table_name, *columns)  # 调用删除记录的函数
        elif command == 'rename' and len(parts) == 4 and parts[1] == 'table':
            rename_table(parts[2], parts[3])
        else:
            print('Invalid command')


if __name__ == '__main__':
    create_table_main()
