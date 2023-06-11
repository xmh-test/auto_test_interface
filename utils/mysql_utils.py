import pymysql
from utils.log_utils import logger


class MysqlUtils:
    @classmethod
    def execute_sql(cls, sql, database_info):
        """
        连接数据库,执行sql语句,获取执行结果
        :param sql: 要执行的sql
        :param database_info: 连接数据库信息
        :return:
        """
        # 连接数据库
        # conn = pymysql.Connect(
        #         host="192.168.50.1",
        #         port=3306,
        #         user="test",
        #         password="test123456",
        #         database="mydb",
        #         charset="utf8mb4"
        #     )
        conn = pymysql.Connect(**database_info)
        cursor = conn.cursor()
        # 执行sql语句
        cursor.execute(sql)
        records = cursor.fetchall()
        logger.debug(f"查询结果:{records}")
        # 关闭数据库连接
        cursor.close()
        conn.close()
        # 返回查询结果
        return records

