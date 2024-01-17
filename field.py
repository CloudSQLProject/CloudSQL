import json
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

    def to_json(self):
        return {
            'name': self.name,
            'data_type': self.data_type,
            'primary_key': self.primary_key,
            'null_flag': self.null_flag
        }

    # JSONEncoder来实现自定义对象的JSON序列化。这需要创建一个自定义的JSON编码器，
    # 并为您的自定义对象实现JSONSerializable接口。
class FieldEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Field):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)

