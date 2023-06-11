import pytest
from apis.contacts.departments import Departments
from utils.utils import Utils


class TestDepartments:
    """
    部门管理接口自动化测试脚本
    """

    def setup_class(self):
        # 实例化部门类
        self.departments = Departments()
        # 准备测试数据
        self.departments.clear()

    @pytest.mark.parametrize(
        "depart_data",
        Utils.get_yaml_data("../data/departments.yaml")
    )
    def test_create_departments_by_params(self, depart_data):
        """
        创建部门单接口测试(参数化)
        :return:
        """
        r = self.departments.create(depart_data.get("data"))
        assert r.status_code == 200
        assert r.json().get("errcode") == depart_data.get("expect")
