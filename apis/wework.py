import os

from apis.base_api import BaseApi
from utils.log_utils import logger
from utils.utils import Utils


class WeWork(BaseApi):
    """
    企业微信特有业务逻辑，完成access_token的获取
    """

    def __init__(self):
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        通过接口获取access_token值
        :return: access_token值
        """
        # 获取环境配置文件
        self.get_config()
        req = {
            "method": "GET",
            "url": f"{self.base_url}/gettoken?corpid={self.corp_id}&corpsecret={self.secret}"
        }
        # 调用封装的发送请求方法
        r = self.send_api(req)
        # 提取响应体中access_token值
        access_token = r.json()["access_token"]
        logger.info(f"获取到access_token值: {access_token}")
        return access_token

    def get_config(self):
        """
        获取yaml文件中的配置信息
        :return:
        """
        # 获取环境变量
        env_info = os.getenv("ENV_TEST", default="test")
        # 读取yaml数据
        yaml_data = Utils.get_yaml_data(f"../config/{env_info}_env.yaml")
        logger.debug(f"yaml文件所有数据: {yaml_data}")
        # 获取需要的值
        self.base_url = yaml_data.get("base_url")
        logger.info(f"读取配置文件的base_url为：{self.base_url}")
        self.corp_id = yaml_data.get("corp_id").get("youlaiyouqu")
        logger.info(f"读取配置文件的corp_id为：{self.corp_id}")
        self.secret = yaml_data.get("secret").get("contacts")
        logger.info(f"读取配置文件的secret为：{self.secret}")


if __name__ == '__main__':
    print(WeWork().access_token)
