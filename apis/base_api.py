import requests
from utils.log_utils import logger


class BaseApi:

    def send_api(self, req):
        """
        对requests二次封装
        :param req: {mehtod: "GET", "url": "http://xxx.com", "params": {}, "json": {}}
        :return:
        """
        logger.info(f"发送请求的信息:{req}")
        r = requests.request(**req)
        logger.info(f"响应数据:{r.text}")
        return r
