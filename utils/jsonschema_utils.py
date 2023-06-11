import json

from genson import SchemaBuilder
from jsonschema.validators import validate
from utils.log_utils import logger


class JsonSchemaUtils:
    @classmethod
    def validate_schema(cls, data_obj, schema):
        """
        通过schema验证数据
        :param data_obj: 要验证的json数据
        :param schema: schema 结构数据
        :return:
        """
        try:
            validate(data_obj, schema=schema)
            return True
        except Exception as e:
            logger.error(f"schema结构体验证失败，失败原因{e}")
            return False

    @classmethod
    def validate_schema_by_file(cls, data_obj, schema_file):
        """
        通过读取schema文件验证json数据
        :param data_obj: 要验证的json数据
        :param schema_file: schema文件路径
        :return: 验证结果
        """
        with open(schema_file, encoding="utf-8") as f:
            schema_data = json.load(f)
        return cls.validate_schema(data_obj, schema_data)

    @classmethod
    def generate_jsonschema(cls, obj):
        """
        将json数据转换成jsonschema数据
        :param obj: 要生产json schema的对象
        :return: json schema数据
        """
        builder = SchemaBuilder()
        # 调用add_object方法，将要转换的数据传入
        builder.add_object(obj)
        # 返回转换成schema结构的数据
        return builder.to_schema()

    @classmethod
    def generate_jsonschema_by_file(cls, obj, file_path):
        """
        生成json schema文件
        :param obj: 要生产json schema的对象
        :param file_path: 保存json schema文件的路径
        :return:
        """
        schema_data = cls.generate_jsonschema(obj)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(schema_data, f)
