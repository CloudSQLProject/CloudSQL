import tkinter as tk
import json
from tkinter import ttk
from select_table import *

# 执行按钮的点击事件处理函数
def execute_button_clicked():
    sql_query = sql_entry.get()  # 获取输入框中的 SQL 语句
    results = execute_sql_query(sql_query)  # 调用相关函数执行 SQL 查询
    display_results_in_table(results)  # 将查询结果显示在表格中
    print(json.dumps(results, indent=2))

# 在表格中显示查询结果
def display_results_in_table(results):
    # 清空表格
    for row in result_tree.get_children():
        result_tree.delete(row)

    # 动态创建表头
    if results:
        headers = list(results[0].keys())
        result_tree['columns'] = headers
        for header in headers:
            result_tree.heading(header, text=header)
        for result in results:
            values = [result[header] for header in headers]
            result_tree.insert('', tk.END, values=values)

# 创建主窗口
root = tk.Tk()
root.title("SQL Query Executor")

# 创建输入框
sql_entry = tk.Entry(root, width=50)
sql_entry.pack(pady=10)

# 创建执行按钮
execute_button = tk.Button(root, text="Execute", command=execute_button_clicked)
execute_button.pack()

# 创建表格
result_tree = ttk.Treeview(root, show="headings")
result_tree.pack()

# 运行主循环
root.mainloop()
