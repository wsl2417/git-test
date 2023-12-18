import allure
import pytest
# from tests.stepdefine import store
from tests.conftest import test_data
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data


class TestOrder:
    def test_order_detail(self, in_data):
        """
        1.用户登录成功，传入正确的token
        2.传入orderNo, 调用接口获取detail信息
        3.断言比较返回状态码，返回message，结果信息包括：
        """
        pass
