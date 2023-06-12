import requests
from requests import Response

from utils.log_utils import logger
import xmltodict


class BaseApi:

    def send_api(self, req):
        """
        对requests二次封装
        :param req: {mehtod: "GET", "url": "http://xxx.com", "params": {}, "json": {}}
        :return:
        """
        # 增加请求超时时间
        req["timeout"] = 5
        logger.info(f"发送请求的信息:{req}")
        r = requests.request(**req)
        logger.info(f"响应数据:{r.text}")
        return r

    def response_to_dict(self, response: Response):
        res_text = response.text
        if res_text.startswith("<?xmh"):
            final_dict = xmltodict.parse(res_text)
        else:
            final_dict = response.json()
        return final_dict
