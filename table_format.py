import json
import os
import field


class Table:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns
        self.data = []
        #注:数据字典,用户名,数据库等属性暂未添加和初始化

    def insert(self, values):
        if len(values) != len(self.columns):
            print("数据列数不匹配!")
            return
        self.data.append(values)

    def save(self):
        directory = "dir/user_default/db0"  # 目标目录
        table_directory = os.path.join(directory, self.table_name)
        if not os.path.exists(table_directory):
            os.makedirs(table_directory)  # 如果目录不存在，就创建目录
        # 如果没有,创建文件,已有文件则追加写入数据
        file_path = os.path.join(table_directory, self.table_name + ".json")
        with open(file_path, 'a' if os.path.exists(self.table_name + ".json") else 'w') as f:# 追加写入数据
            init_data=[]
            json.dump(init_data,f)
            for row in self.data:
                print(row)
                print("-----------")
                value_str=','.join(map(str, row.values()))
                f.write(value_str+'\n')
            print("表数据写入成功!")
        dict_path = os.path.join(table_directory, self.table_name + "_struct.json")
        if not os.path.exists(dict_path):
            with open(dict_path, 'w') as f:
                init_dict=[]
                for column in self.columns:
                    init_dict.append(column)
                json.dump(init_dict,f,cls=field.FieldEncoder,indent=4)


                    #f.write(f"name: {column.name},data_type: {column.data_type},primary_key: {column.primary_key},null_flag: {column.null_flag}\n")

