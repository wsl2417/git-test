import allure
import pytest
from tests.stepdefine import store
from tests.conftest import test_data
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data

modify_data = combine_case_data(test_data, 'test_modify_store_info')
base_info = combine_case_data(test_data, 'test_get_base_info')


@allure.step("断言 ==>> 接口返回结果验证")
def step_assert(expect_code, response_code):
    logger.info("返回code ==> 期望结果：{}, 实际结果： [{}]".format(expect_code, response_code))


@allure.step("发送更新门店信息请求")
def step_update(update_dict):
    logger.debug("更新门店信息数据: {}".format(update_dict))


@allure.step("前置步骤 ==> 获取门店信息")
def pre_step(token):
    origin_info = store.get_base_info(token)
    logger.info("更新前门店信息为：{}".format(origin_info))


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("门店模块")
class TestStoreInfo:
    @allure.story("门店信息接口测试")
    @pytest.mark.smoke
    @pytest.mark.parametrize("update_info_dict, expect_result, expect_msg, expect_code, title",
                             modify_data)
    def test_modify_store_info(self, login_fixture, update_info_dict, expect_result, expect_msg, expect_code, title):
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        with allure.step("前置步骤一 ==> 用户登录"):
            token = login_fixture
        with allure.step("前置步骤二 ==> 获取门店基本信息"):
            origin_info = store.get_base_info(token)
            logger.info("更新前门店信息为: {}".format(origin_info))
        update_data = {"token": token}
        if modify_data:
            for key, value in update_info_dict.items():
                # if origin_info.get(key):
                logger.info("更新字段: {}, 值更新为：{}".format(key, value))
                update_data[key] = value
        else:
            logger.info("门店信息没有更新")
        step_update(update_data)
        result = store.modify_store_info(token, update_data)
        assert result.success == expect_result, result.error
        step_assert(expect_code, result.code)
        assert result.code == expect_code
        assert expect_msg in result.msg

    @allure.story("获取门店基本信息接口")
    @pytest.mark.smoke
    @pytest.mark.parametrize(",expect_result, expect_msg, expect_code, title", base_info)
    def test_get_base_info(self, login_fixture, expect_result, expect_msg, expect_code, title):
        """
        获取门店基本信息接口测试集
        """
        allure.dynamic.title(title)
        with allure.step("前置步骤 ==> 用户登录"):
            token = login_fixture
        with allure.step("测试接口 ==> 获取门店基本信息"):
            result = store.get_base_info(token)
        assert result.success == expect_result, result.error
        step_assert(expect_code, result.code)
        assert result.code == expect_code
        assert expect_msg in result.msg


# if __name__ == "__main__":
#     pytest.main()
