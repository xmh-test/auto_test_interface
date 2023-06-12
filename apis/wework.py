import os

from apis.base_api import BaseApi
from utils.log_utils import logger
from utils.utils import Utils


class WeWork(BaseApi):
    """
    企业微信特有业务逻辑，完成access_token的获取
    """

    def __init__(self):
        self.base_url = None
        self.corp_id = None
        self.secret = None
        self.request_timeout = None
        self.proxy_status = None
        self.proxies = None
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
            "url": f"/gettoken",
            "params": {"corpid": self.corp_id, "corpsecret": self.secret}
        }
        # 调用封装的发送请求方法
        r = self.send_api(req, token_status=0)
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
        logger.debug(f"读取配置文件的base_url为：{self.base_url}")
        self.corp_id = yaml_data.get("corp_id").get("youlaiyouqu")
        logger.debug(f"读取配置文件的corp_id为：{self.corp_id}")
        self.secret = yaml_data.get("secret").get("contacts")
        logger.debug(f"读取配置文件的secret为：{self.secret}")
        self.request_timeout = yaml_data.get("request_timeout")
        logger.debug(f"读取配置文件的request_timeout为：{self.request_timeout}")
        self.proxy_status = yaml_data.get("proxy_status")
        if self.proxy_status == 1:
            self.proxies = yaml_data.get("proxies")
            logger.debug(f"读取配置文件的proxies为：{self.proxies}")
        else:
            logger.debug("代理状态：未启用")

    def send_api(self, req: dict, token_status: int = 1):
        """
        重写父类send_api方法，增加默认超时，代理配置等
        :param token_status: 是否添加token信息，1： 添加、其他值不添加
        :param req: {"mehtod": "GET", "url": "http://xxx.com", "params": {}, "json": {}， "proxies": None, "verify": False}
        :return:
        """
        # 添加base_url
        path = req.get("url")
        if not path.lower().startswith('http'):
            req["url"] = self.base_url + path

        # 添加token信息
        if token_status == 1:
            params = req.get("params")
            if params is None:
                req["params"] = {"access_token": self.access_token}
            else:
                req["params"]["access_token"] = self.access_token

        # 添加代理配置
        if self.proxy_status == 1:
            req["proxies"] = self.proxies
            req["verify"] = False

        return super().send_api(req)


if __name__ == '__main__':
    ww = WeWork()
    # print(ww.access_token)
    data = {'name': '技术部', 'name_en': 'JISHU1', 'parentid': 1, 'order': 1, 'id': 2}
    req = {
        "method": "POST",
        "url": f"/department/create",
        "json": data
    }
    ww.send_api(req)
