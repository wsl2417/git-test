import allure
import pytest
# 引用要调用的接口调用步骤
from tests.stepdefine import store
# 在conftest中读取了yaml里的用例数据，这里需要引用读取的yaml数据
from tests.conftest import test_data
# 引用日志模块以打印debug/info log
from Libraries.log_generator.logger import logger
# 这个方法用来将读取到的yaml数据转换成输入test_xx函数的输入数据列表，解析后可以直接传参
from Libraries.read_data.phase_yaml_to_param import combine_case_data

# 根据yaml中的用例数据key取到当前测试用例需要的数据
modify_data = combine_case_data(test_data, 'test_modify_store_info')


@allure.step("断言 ==>> 接口返回结果验证")
def step_assert(expect_code, response_code):
    # 定义一个allure步骤，这个步骤在test用例中调用后将会显示在allure报告中
    logger.info("返回code ==> 期望结果：{}, 实际结果： [{}]".format(expect_code, response_code))


@allure.step("发送更新门店信息请求")
def step_update(update_dict):
    logger.debug("更新门店信息数据: {}".format(update_dict))


@allure.step("前置步骤 ==> 获取门店信息")
def pre_step(token):
    origin_info = store.get_base_info(token)
    logger.info("更新前门店信息为：{}".format(origin_info))


@allure.severity(allure.severity_level.CRITICAL)    # 定义用例重要等级，在allure报告中显示, 非必填，建议加上
@allure.epic("蛋挞平台接口测试")                       # 定义allure报告的epic名，必填
@allure.feature("门店模块")                          # 定义allure报告的feature名，必填
class TestStoreInfo:                                # pytest测试类集，可以编写多个测试用例，必须以Test开头且不能有__init__方法
    @allure.story("门店信息接口测试")                  # 定义allure报告storey名，必填
    @pytest.mark.smoke                              # 设置用例标签，便于区分用例重要等级，菲必填，建议加上
    @pytest.mark.parametrize("update_info_dict, expect_result, expect_msg, expect_code, title",
                             modify_data)           # pytest参数化方法，用来传递用例数据列表，具体定义和使用可以搜pytest手册
    def test_modify_store_info(self, login_fixture, update_info_dict, expect_result, expect_msg, expect_code, title):# pytest测试用例套件，多少条用例数据就有多少条用例
        allure.dynamic.title(title)                 # 根据每组输入数据的title，自定义生成该用例的allure标题，必填
        logger.info("==========开始执行用例=========")
        with allure.step("前置步骤一 ==> 用户登录"):
            token = login_fixture                                       # 调用conftest中定义的login_fixture来获取用户登录token(注意这是一个夹具，不是函数所以调用时需要在传参中传入，且后面不带括号）
        with allure.step("前置步骤二 ==> 获取门店基本信息"):
            origin_info = store.get_base_info(token)                    # 获取更新前的门店基本信息，便于debug
            logger.info("更新前门店信息为: {}".format(origin_info))
        update_data = {"token": token}
        if modify_data:
            for key, value in update_info_dict.items():                 # 如果输入的数据非空，表示有门店信息更新，则打印更新字段
                # if origin_info.get(key):
                logger.info("更新字段: {}, 值更新为：{}".format(key, value))
                update_data[key] = value
        else:                                                           # 输入数据为空，就表示没有发送更新消息，值传递了token给更新门店信息接口，表示无更新
            logger.info("门店信息没有更新")
        with allure.step("发送更新门店信息请求"):
            step_update(update_data)                                    # 调用更新门店接口，发送测试数据
        result = store.modify_store_info(token, update_data)            # 获取接口返回值对象
        assert result.success == expect_result, result.error            # 对返回结果进行断言，可自定义期望值
        step_assert(expect_code, result.code)
        assert result.code == expect_code
        assert expect_msg in result.msg
