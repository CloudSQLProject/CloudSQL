import tkinter as tk
from tkinter import messagebox, ttk
import json
from select_table import execute_sql_query

#select * from student inner join grade on name where score>89
#select * from student inner join grade on name
#select * from student where age>20
#select * from student order by age asc
#select name,age from student
#select name,age,score,id from student inner join grade on name where score>89 order by age asc


def validate_login(username, password):
    with open('users.json') as f:
        users = json.load(f)
        if username in users and users[username]['password'] == password:
            return True
    return False

def display_results_in_table(results, result_tree):
    for row in result_tree.get_children():
        result_tree.delete(row)

    if results:
        headers = list(results[0].keys())
        result_tree['columns'] = headers
        for header in headers:
            result_tree.heading(header, text=header)
            result_tree.column(header, anchor="center")
        for result in results:
            values = [result[header] for header in headers]
            result_tree.insert('', tk.END, values=values)

def login_button_clicked(username_entry, password_entry, root):
    username = username_entry.get()
    password = password_entry.get()
    if validate_login(username, password):
        root.destroy()
        create_main_window()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def execute_button_clicked(sql_entry, result_tree):
    sql_query = sql_entry.get()
    results = execute_sql_query(sql_query)
    display_results_in_table(results, result_tree)
    print(json.dumps(results, indent=2))

def create_main_window():
    root = tk.Tk()
    root.title("SQL Query Executor")

    sql_entry = tk.Entry(root, width=100)
    sql_entry.pack(pady=10)

    execute_button = tk.Button(root, text="Execute", command=lambda: execute_button_clicked(sql_entry, result_tree))
    execute_button.pack()

    result_tree = ttk.Treeview(root, show="headings")
    result_tree.pack()

    root.mainloop()

root = tk.Tk()
root.title("Login")
root.geometry("300x150")

frame = tk.Frame(root)
frame.pack(pady=20)

username_label = tk.Label(frame, text="Username")
username_label.grid(row=0, column=0)
username_entry = tk.Entry(frame)
username_entry.grid(row=0, column=1)

password_label = tk.Label(frame, text="Password")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(frame, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(root, text="Login", command=lambda: login_button_clicked(username_entry, password_entry, root))
login_button.pack()

root.mainloop()
