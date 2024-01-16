import tkinter as tk
import json
from tkinter import ttk
from select_table import *

def extract_headers_from_json(data):
    if isinstance(data, list) and len(data) > 0:
        headers = list(data[0].keys())
        return headers
    else:
        return []
 # 这里假设执行查询后得到的结果是一个列表，每个元素是一个字典
results = []

# 模拟的函数，根据SQL查询返回JSON结果
def execute_sql_query(sql):
    results =
    # headers = extract_headers_from_json(results)
    # print(headers)
    return results

# 执行按钮的点击事件处理函数
def execute_button_clicked():
    sql_query = sql_entry.get()  # 获取输入框中的SQL语句
    results = execute_sql_query(sql_query)  # 调用相关函数执行SQL查询
    display_results_in_table(results)  # 将查询结果显示在表格中
    print(json.dumps(results, indent=2))


# 在表格中显示查询结果
def display_results_in_table(results):
    # 清空表格
    for row in result_tree.get_children():
        result_tree.delete(row)

    # 在表格中插入数据
    for result in results:
        result_tree.insert('', tk.END, values=tuple(result.values()))

# 创建主窗口
root = tk.Tk()
root.title("SQL Query Executor")

# 创建输入框
sql_entry = tk.Entry(root, width=50)
sql_entry.pack(pady=10)

# 创建执行按钮
execute_button = tk.Button(root, text="Execute", command=execute_button_clicked)
execute_button.pack()


headers = extract_headers_from_json(results)
print(headers)
# 创建表格h
result_tree = ttk.Treeview(root, columns=headers, show="headings")
for head in headers:
    result_tree.heading(head, text=head)

result_tree.pack()

# 运行主循环
root.mainloop()