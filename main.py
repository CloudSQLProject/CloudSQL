import json
import os
from create_table import *
from select_table import *
from update_table import *
loginFlag = False


def create_user_database():
    if not os.path.exists('./users.json'):
        with open('./users.json', 'w') as file:
            initial_data = {'root': {'password': 'root', 'type': 1}}
            json.dump(initial_data, file)

def login(username, password):
    with open('./users.json', 'r') as file:
        users = json.load(file)
        if username in users :
            if users[username]['password'] == password:
                print('Login successful. User type:', users[username]['type'])
                user_type = users[username]['type']
                return True, user_type
            else:
                print(f'User {username} Wrong Password')
                return False, 0
        else:
            print(f'User {username} Not Found')
            return False, 0

def add_user(username, password):
    global loginFlag, user_type
    if loginFlag:
        if user_type == 1:
            with open('./users.json', 'r') as file:
                users = json.load(file)
                if username in users:
                    print('User already exists')
                    return
                users[username] = {'password': password, 'type': 0}
                with open('./users.json', 'w') as file:
                    json.dump(users, file, indent=4)
                print('User added successfully')
        else:
            print('Low Authorization')
    else:
        print('Please login first')


def grant_authorization(username):
    global loginFlag, user_type
    if loginFlag:
        if user_type == 1:
            with open('./users.json', 'r') as file:
                users = json.load(file)
                if username in users:
                    users[username]['type'] = 1
                    with open('./users.json', 'w') as file:
                        json.dump(users, file, indent=4)
                    print(f'Authorization granted to {username}')
                else:
                    print(f'User {username} not found')
        else:
            print('Low Authorization')
    else:
        print('Please login first')


def drop(username):
    global loginFlag, user_type
    if loginFlag:
        if user_type == 1:
            with open('./users.json', 'r') as file:
                users = json.load(file)
                if username in users:
                    del users[username]
                    with open('./users.json', 'w') as file:
                        json.dump(users, file, indent=4)
                    print(f'{username} Deleted')
                else:
                    print(f'User {username} not found')
        else:
            print('Low Authorization')
    else:
        print('Please login first')



if __name__ == "__main__":
    create_user_database()
    while True:
        command = input()
        if command.startswith("login"): #登录
            _, username, password = command.split()
            loginFlag, user_type = login(username, password)
            if loginFlag:
                print('Welcome to the database')

        elif command.startswith("add_user"): #添加用户
            _, username, password = command.split()
            add_user(username, password)

        elif command.startswith("grant"): #赋予权限
            _, username = command.split()
            grant_authorization(username)

        elif command.startswith("drop"): #删除用户
            _, username = command.split()
            drop(username)

        elif command.startswith("exit"): #退出
            loginFlag = False
            break
        elif command.startswith("table"):
            create_table_main()
