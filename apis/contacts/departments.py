from apis.wework import WeWork
from jsonpath import jsonpath


class Departments(WeWork):
    """
    通讯录部门管理
    """

    def create(self, data: dict):
        """
        创建部门
        :param data: {"name": "广州研发中心","name_en": "RDGZ","parentid": 1,"order": 1,"id": 2}
        :return:
        """
        req = {
            "method": "POST",
            "url": "/department/create",
            "json": data
        }
        return self.send_api(req)

    def update(self, data: dict):
        """
        通过id更新部门信息
        :param data:
        :return:
        """
        req = {
            "method": "POST",
            "url": "/department/update",
            "json": data
        }
        return self.send_api(req)

    def delete(self, depart_id):
        """
        通过depart_id删除部门
        :param depart_id: 部门id
        :return:
        """
        req = {
            "method": "GET",
            "url": f"/department/delete",
            "params": {"id": depart_id}
        }
        return self.send_api(req)

    def get_all(self):
        """
        获取部门ID
        :return:
        """
        req = {
            "method": "GET",
            "url": "/department/simplelist"
        }
        return self.send_api(req)

    def get_info(self, depart_id):
        """
        获取单个部门的详情
        :param depart_id: 部门id
        :return:
        """
        req = {
            "method": "GET",
            "url": f"/department/get",
            "params": {"id": depart_id}
        }
        return self.send_api(req)

    def clear(self):
        """
        清除其他部门,仅保留id为1的部门
        :return:
        """
        # 获取所有部门id
        depart_ids = jsonpath(self.get_all().json(), "$..id")
        # 保留id=1的部门,其他都删除
        for depart_id in depart_ids:
            if depart_id != 1:
                # 调用删除部门接口
                self.delete(depart_id)
