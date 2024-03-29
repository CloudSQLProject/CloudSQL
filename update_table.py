import copy
import json
import os
import re
from select_table import apply_condition
from shared_data import table_keys, table_columns


def type_legal(value, key):
    if key == 'int':
        if re.match('(\+|\-)?[0-9]+$', value) or value == '':  # value 可以== ''， 检查其是否有约束 not null
            return True
        else:
            return False
    if key == 'varchar(20)':
        if re.match("(.+)?$", value):
            return True
        else:
            return False
    if key == 'char':
        if re.match("'(.+)?'$", value) and len(value) <= 3:
            return True
        else:
            return False
    if key == 'double':
        if re.match('(\+|\-)?[0-9]+\.?[0-9]+$', value) or value == '':
            return True
        else:
            return False
    return False


def get_nature_and_type_from_dictionary(table_name):
    """ 从字典中获取表的字段名和属性 """
    dictionary = {}
    directory = "dir/user_default/db0"  # 目标目录
    table_directory = os.path.join(directory, table_name)
    table_file = table_directory + f'/{table_name}_struct.json'
    with open(table_file) as f:
        contents = json.load(f)
    for content in contents:
        dictionary[content['name']] = content['data_type']
    return dictionary
    # for item in dbms_settings.dictionary[dbms_settings.current_database]['tables'][table_name]['items']:
    #     nature_arr.append(item['nature'])
    #     type_arr.append(item['type'])


# 是select_column, 若update语句有where条件，则查询，修改查询结果，在写回文件
# 如果select_column有return可以直接使用select_column
def update_select(table_name, aim, where_condition):
    if table_name in table_keys:
        primary_key = table_keys[table_name]
        if primary_key not in aim:
            aim.insert(0, primary_key)
    else:
        print(f"Error: Table {table_name} not found in table_keys")
        return
    directory = "dir/user_default/db0"  # 目标目录
    table_directory = os.path.join(directory, table_name)
    table_file = table_directory + f'/{table_name}.json'
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
    return result


# 无where条件语句时
def update_all(table_name,
               natures):  # 例：(update table_name set key1=value1,key2=value2) <--natures=key1=value1,key2=value2
    pairs = natures.split(',')  # 逗号分隔
    directory = "dir/user_default/db0"  # 目标目录
    table_directory = os.path.join(directory, table_name)
    table_file = table_directory + f'/{table_name}.json'
    my_dict = get_nature_and_type_from_dictionary(table_name)
    with open(table_file, 'r') as f:
        contents = json.load(f)
    for pair in pairs:
        key, value = pair.strip().split('=')  # 键值对
        if key in my_dict.keys():
            if type_legal(value, my_dict[key]):
                for content in contents:
                    content[key.strip()] = value.strip()  # 遍历所有结果并赋值
            else:
                print(f'type error: {key} want {my_dict[key]} ')
                return
        else:
            print(f'the column {key} does not exist')
            return
    with open(table_file, 'w') as f:
        json.dump(contents, f, indent=4)
        print(f'update successful:{len(contents)} rows updated')


def update_part(table_name, condition,
                natures):  # 例：(update table_name set key1=value1,key2=value2 where condition) <--natures=key1=value1,key2=value2
    directory = "dir/user_default/db0"  # 目标目录
    table_directory = os.path.join(directory, table_name)
    table_file = table_directory + f'/{table_name}.json'
    pairs = natures.split(',')
    contents = update_select(table_name, table_columns[table_name], [[condition]])  # select执行结果
    my_dict = get_nature_and_type_from_dictionary(table_name)
    with open(table_file, 'r') as f:
        responses = json.load(f)
    for pair in pairs:
        key, value = pair.strip().split('=')
        if key in my_dict.keys():
            if type_legal(value, my_dict[key]):
                for content in contents:
                    content[key.strip()] = value.strip()  # 赋值
            else:
                print(f'type error: {key} want {my_dict[key]} ')
                return
        else:
            print(f'the column {key} does not exist')
            return
    for i, response in enumerate(responses):  # responses是文件内容 content是修改后的select结果
        for content in contents:
            if response['id'] == content['id']:
                responses[i] = copy.deepcopy(content)  # 遍历并按id位置写回
                break
    with open(table_file, 'w') as f:
        json.dump(responses, f, indent=4)
        print(f'update successful:{len(contents)} rows updated')


def handle_update_sql()->None:
    while True:
        sql = input("Enter Command:")
        """ 分析 update 语法"""
        is_all = False
        table_name = ''
        condition = ''
        natures = ''
        pattern_one = 'update ([a-z0-9_]+) set (.+) where (.+)'
        pattern_two = 'update ([a-z0-9_]+) set (.+)'
        if not re.match(pattern_one, sql):
            if not re.match(pattern_two, sql):
                print("command error ")
                return
            else:
                is_all = True
                table_name = re.match(pattern_two, sql).group(1)
                natures = re.match(pattern_two, sql).group(2)
        else:
            table_name = re.match(pattern_one, sql).group(1)
            natures = re.match(pattern_one, sql).group(2)
            condition = re.match(pattern_one, sql).group(3)
        if not os.path.exists(f'./dir/user_default/db0/{table_name}/{table_name}.json'):
            print('Table does not exist')
        # 更新全部数据
        if is_all:
            update_all(table_name, natures)
        else:
            # where p = q
            update_part(table_name, condition, natures)
            return

# 正确情况
# handle_update_sql("update student set name='gentleman',age=22 where id<3")
# handle_update_sql("update student set name='zhao_shuai',age=23")

# 错误情况
# handle_update_sql("update student set name='TOM',age='Alice' where id=1")
# 提示age want int