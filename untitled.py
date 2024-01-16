import tkinter as tk
from tkinter import messagebox
import json
from select_table import *
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
        print (conditions)
    return conditions


def apply_condition(row, condition):
    if isinstance(condition, list):
        return any(apply_condition(row, sub_condition) for sub_condition in condition)
    match = re.match(r'(\w+)\s*([<>=]+)\s*(\w+)', condition)
    if match:
        condition_key, condition_op, condition_value = match.groups()
        condition_key = condition_key.strip()
        condition_value = condition_value.strip()
        row_value = row.get(condition_key)
        if row_value is not None:
            if condition_op == '=':
                return row_value == condition_value
            elif condition_op == '<':
                return row_value < condition_value
            elif condition_op == '>':
                return row_value > condition_value
            elif condition_op == '>=':
                return row_value >= condition_value
            elif condition_op == '<=':
                return row_value <= condition_value
    return False



def get_user_input(user_input):
    global conditions
    parts = user_input.split(' ')
    if len(parts) < 4 or parts[0].lower() != 'select' or parts[2].lower() != 'from':
        print("Invalid command")
        return None,None,None,None,None
    else:
        aim = parts[1].split(',')
        table = parts[3]
        where_condition = None
        order_by_column = None
        order_by_order = None
        if len(parts)>4 and parts[4].lower() == 'where':
            where_condition = ' '.join(parts[5:])
            conditions = parse_where_conditions(where_condition)
            #print(conditions)
        if 'order' in parts and 'by' in parts:
            order_by_index = parts.index('order')
            order_by_column = parts[order_by_index + 2]
            order_by_order = parts[order_by_index + 3] if order_by_index + 3 < len(parts) else 'asc'
        return aim,table,conditions, order_by_column, order_by_order

def get_user_input_inner_join(user_input):
    global conditions
    select_match = re.search(r'select (.*?) from', user_input, re.I)
    where_match = re.search(r'where (.*)', user_input, re.I)
    order_by_match = re.search(r'order by (.*)', user_input, re.I)
    if select_match and where_match:
        aim = select_match.group(1).split(',')
        where_condition = where_match.group(1)
        conditions = parse_where_conditions(where_condition)
        #print(conditions)
        order_by_column = None
        order_by_order = None
        if order_by_match:
            order_by_info = order_by_match.group(1).split()
            order_by_column = order_by_info[0]
            order_by_order = order_by_info[1] if len(order_by_info) > 1 else 'asc'
            #print(order_by_column, order_by_order)
        return aim, conditions, order_by_column, order_by_order
    else:
        print("Invalid command")
        return None, None, None, None


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


def select_all(table_name,where_condition,order_by_column, order_by_order):
    return select_column(table_name,table_columns[table_name],where_condition,order_by_column, order_by_order)


def inner_join(table1, table2, join_key, select_fields, where_condition, order_by_column, order_by_order):
    with open(f'{table1}.json') as f1, open(f'{table2}.json') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    result = []
    for row1 in data1:
        for row2 in data2:
            if row1[join_key] == row2[join_key]:
                combined_row = {**row1, **row2}
                if not where_condition or all(apply_condition(combined_row, condition) for condition in where_condition):
                    if select_fields == ['*']:
                        result_row = combined_row
                    else:
                        result_row = {field: combined_row[field] for field in select_fields}
                    result.append(result_row)
    if order_by_column:
        result.sort(key=lambda x: x.get(order_by_column, 0), reverse=(order_by_order.lower() == 'desc'))
    keys = result[0].keys() if result else []
    max_lengths = [len(str(key)) for key in keys]
    rows = []
    for row in result:
        values = list(row.values())
        rows.append(values)
        max_lengths = [max(max_lengths[i], len(str(values[i])) if values[i] else 0) for i in range(len(values))]

    draw_table(rows, keys, max_lengths)



def select_column(table_name, aim, where_condition,order_by_column, order_by_order):
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
        if order_by_column:
            result.sort(key=lambda x: x.get(order_by_column, 0))
            if order_by_order.lower() == 'desc':
                result.reverse()
        keys = result[0].keys() if result else []
        max_lengths = [len(str(key)) for key in keys]
        rows = []
        for row in result:
            values = list(row.values())
            rows.append(values)
            max_lengths = [max(max_lengths[i], len(str(values[i])) if values[i] else 0) for i in range(len(values))]
        draw_table(rows, keys, max_lengths)


def extract_tables_from_inner_join(user_input):
    match_with_where = re.search(r'select (.*?) from (\w+) inner join (\w+) on (\w+) where (.*)', user_input, re.I)
    match_without_where = re.search(r'select (.*?) from (\w+) inner join (\w+) on (\w+)', user_input, re.I)
    if match_with_where:
        select_content, table1, table2, key, where_content = match_with_where.groups()
        return select_content, table1, table2, key, where_content
    elif match_without_where:
        select_content, table1, table2, key = match_without_where.groups()
        return select_content, table1, table2, key, None
    else:
        return None, None, None, None, None




def compare_user_info(username, password):
    with open('./users.json', 'r') as file:
        data = json.load(file)
        if username in data:
            if data[username]['password'] == password:
                messagebox.showinfo("登录成功", "欢迎，" + username + "!")
                open_sql_page()
            else:
                messagebox.showerror("登录失败", "密码错误")
        else:
            messagebox.showerror("登录失败", "用户名不存在")

def login():
    username = username_entry.get()
    password = password_entry.get()
    compare_user_info(username, password)

def open_sql_page():
    root.withdraw()
    sql_page = tk.Tk()
    sql_page.title("SQL查询")

    query_label = tk.Label(sql_page, text="输入SQL语句：")
    query_label.pack()
    query_entry = tk.Entry(sql_page)
    query_entry.pack()

    result_label = tk.Label(sql_page, text="查询结果：")
    result_label.pack()
    result_text = tk.Text(sql_page, height=10, width=50)
    result_text.pack()

    def run_query():
        sql_query = query_entry.get()
        if 'inner join' in sql_query.lower():
            select_content, table1, table2, key, where_content = extract_tables_from_inner_join(sql_query)
            if select_content and table1 and table2 and key:
                select_fields, conditions, order_by_column, order_by_order = get_user_input_inner_join(sql_query)
                result = inner_join(table1, table2, key, select_fields, conditions, order_by_column, order_by_order)
                display_result(result)
            else:
                display_invalid_query_message()
        else:
            aim, table, conditions, order_by_column, order_by_order = get_user_input(sql_query)
            if aim and table:
                if conditions:
                    result = select_column(table, aim, conditions, order_by_column, order_by_order)
                    display_result(result)
                else:
                    result = select_all(table, None, order_by_column, order_by_order)
                    display_result(result)
            else:
                display_invalid_query_message()

    def display_result(result):
        result_text.delete('1.0', tk.END)
        if result:
            for row in result:
                result_text.insert(tk.END, "|".join(map(str, row)) + "\n")
        else:
            result_text.insert(tk.END, "No results found")

    def display_invalid_query_message():
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Invalid query")

    query_button = tk.Button(sql_page, text="执行查询", command=run_query)
    query_button.pack()

    result_text = tk.Text(sql_page, height=10, width=50)
    result_text.pack()

    def close_sql_page():
        sql_page.destroy()
        root.deiconify()

    sql_page.protocol("WM_DELETE_WINDOW", close_sql_page)
    sql_page.mainloop()

# 创建主窗口
root = tk.Tk()
root.title("登录系统")

# 添加用户名和密码输入框
username_label = tk.Label(root, text="用户名：")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(root, text="密码：")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# 添加登录按钮
login_button = tk.Button(root, text="登录", command=login)
login_button.grid(row=2, columnspan=2, padx=10, pady=10)

# 设置窗口大小
root.geometry("400x300")
# 设置输入框居中
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


# 运行主循环
root.mainloop()
