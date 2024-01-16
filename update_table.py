import copy
import json
import os
import re


from CloudSQL.select_table import  apply_condition
from CloudSQL.shared_data import table_keys,table_columns


def update_select(table_name, aim, where_condition):    # 同select_column, 将select结果更新并写回
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
        print("--------------------------------")
        print(response)
        print("--------------------------------")
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

def update_all(table_name, natures):
    pairs = natures.split(',')
    with open(f'{table_name}.json', 'r+') as f:
        contents = json.load(f)
    for nv in pairs:
        key, value = nv.strip().split('=')
        for content in contents:
            content[key.strip()] = value.strip()
    with open(f'{table_name}.json', 'r+') as f:
        json.dump(contents, f, indent=4)


def update_part(table_name, condition, natures):
    pairs = natures.split(',')
    contents = update_select(table_name, table_columns[table_name],[[condition]])
    with open(f'{table_name}.json', 'r+') as f:
        responses = json.load(f)
    for pair in pairs:
        key, value = pair.strip().split('=')
        for content in contents:
            content[key.strip()] = value.strip()
    for i, response in enumerate(responses):
        for content in contents:
            if response['id'] == content['id']:
                responses[i] = copy.deepcopy(content)
                break
    with open(f'{table_name}.json', 'r+') as f:
        json.dump(responses, f, indent=4)


def handle_update_sql(sql):
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
    # 判断表是否存在，view 未做处理...
    # if table_name not in dbms_settings.dictionary[dbms_settings.current_database]['tables']:
    #     print("Table doesn't exist")
    #     return
    if not os.path.exists(f'{table_name}.json'):
        print('Table does not exist')
    # 更新全部数据
    if is_all:
        update_all(table_name, natures)
    else:
        # where p = q
        update_part(table_name, condition, natures)
        return

handle_update_sql("update student set name='zhaoshuai',age=88 where id<3")
# handle_update_sql("update student set name='zhaoshuai',age=565")

