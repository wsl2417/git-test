import allure
import pytest
import yaml
from tests.conftest import test_get_data
from danta_common.api.store import store
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.stepdefine.pending_get_order_list import pending_order_list

ifo_data, ids = combine_case_data(test_get_data, 'test_get_order_list')

@allure.step("断言 === 》 接口返回验证结果")
def  step_assert(expect_code,response_code):
    logger.info("返回code ==> 期望结果：{}, 实际结果： [{}]".format(expect_code,response_code))


@allure.step("前置步骤===》获取门店基本信息")
def orderlist_2(token):
    origin_info = store.get_base(token)
    logger.info("获取门店信息为：{}".format(origin_info))



@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("pos收银模块")
class TestUserLogin:
    @allure.story("获取挂单列表")
    @pytest.mark.smoke
    @pytest.mark.parametrize("expect_result, expect_msg, expect_code, title", ifo_data, ids=ids)
    def test_pending_get_order_list(self,get_store_success, expect_result, expect_msg, expect_code, title):
        """
        步骤一
        该test用来测试有挂单数据进入获取挂单列表
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, storeId = get_store_success
        result_object = pending_order_list(token, str(storeId))
        logger.info(result_object.result)

        assert result_object == expect_code
        logger.info("==========用例执行结束=========")