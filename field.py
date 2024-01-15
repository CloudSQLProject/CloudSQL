class Field:
    """
           构造函数，用于初始化表的列对象

           参数：
           - name: 列名
           - data_type: 列的数据类型
           - primary_key: 是否为主键，布尔值
           - not_null: 是否允许为空，布尔值
           """
    def __init__(self, name, data_type, primary_key, null_flag):#
        self.name = name
        self.data_type = data_type
        self.primary_key = primary_key
        self.null_flag = null_flag

