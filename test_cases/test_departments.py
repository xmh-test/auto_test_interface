import allure
from apis.contacts.departments import Departments
from jsonpath import jsonpath
from utils.jsonschema_utils import JsonSchemaUtils


@allure.feature("部门管理接口测试用例")
class TestDepartments:
    """
    部门管理接口自动化测试脚本
    """

    def setup_class(self):
        # 实例化部门类
        self.departments = Departments()
        # 准备测试数据
        self.depart_id = 210
        self.create_data = {
            "name": "技术部",
            "name_en": "JISHU1",
            "parentid": 1,
            "order": 1,
            "id": self.depart_id
        }
        self.update_name = "技术部-update"
        self.update_data = {
            "name": self.update_name,
            "id": self.depart_id
        }
        self.departments.clear()

    @allure.story("部门增改查删场景用例")
    def test_departments_flow(self):
        """
        部门增改查删场景用例
        """

        with allure.step("创建部门"):
            # 创建部门
            r = self.departments.create(self.create_data)
            assert r.status_code == 200
            assert r.json().get("errcode") == 0

        with allure.step("查询是否创建成功"):
            # 查询是否创建成功
            r = self.departments.get_all()
            # 在响应体中提取所有部门id
            # 使用常规dict获取方法
            # depart_ids = [d.get("id") for d in r.json().get("department_id")]
            # 使用jsonpath获取方法
            depart_ids = jsonpath(r.json(), "$..id")
            assert self.depart_id in depart_ids

        with allure.step("更新部门"):
            # 更新部门
            r = self.departments.update(self.update_data)
            assert r.status_code == 200
            assert r.json().get("errcode") == 0

        # 查询是否更新成功
        # # 腾讯变更安全规则,该功能不可用
        # r = self.departments.get_info(self.depart_id)
        # assert r.status_code == 200
        # assert r.json().get("errcode") == 0
        # assert r.json().get("department").get("name") == self.update_name

        with allure.step("删除部门"):
            # 删除部门
            r = self.departments.delete(self.depart_id)
            assert r.status_code == 200
            assert r.json().get("errcode") == 0

        with allure.step("查询是否删除成功"):
            # 查询是否删除成功
            r = self.departments.get_all()
            depart_ids = jsonpath(r.json(), "$..id")
            assert self.depart_id not in depart_ids

    @allure.story("查询部门接口用例")
    def test_get_departments_schema(self):
        """
        测试查询部门接口,使用jsonschema验证结果
        """
        # 预期数据结构
        expect = {
            "errcode": 0,
            "errmsg": "ok",
            "department_id": [
                {
                    "id": 2,
                    "parentid": 1,
                    "order": 10
                },
                {
                    "id": 3,
                    "parentid": 2,
                    "order": 40
                }
            ]
        }
        # 生成jsonschema文件
        schema_file = "../data/schema/get_departments_schema.json"
        JsonSchemaUtils.generate_jsonschema_by_file(expect, schema_file)
        # 发出查询请求
        r = self.departments.get_all()
        # 断言响应体结构
        assert JsonSchemaUtils.validate_schema_by_file(r.json(), schema_file)
