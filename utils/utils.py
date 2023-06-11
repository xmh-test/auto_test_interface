import os
import yaml


class Utils:

    @classmethod
    def get_yaml_data(cls, file_path):
        """
        读取yaml文件
        :param file_path: yaml文件路径
        :return: yaml文件数据
        """
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    @classmethod
    def get_frame_root_path(cls):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    print(Utils.get_yaml_data("../data/departments.yaml"))
    db_info = {
        "host": "192.168.50.1",
        "port": 3306,
        "user": "test",
        "password": "test123456",
        "database": "mydb",
        "charset": "utf8mb4"
    }
