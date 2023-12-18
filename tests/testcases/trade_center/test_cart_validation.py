import pytest
import allure
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.conftest import test_data
from tests.stepdefine import cart_operation
from tests.stepdefine import user_center
from danta_common import COMMON_CONFIG

in_data = combine_case_data(test_data, "test_add_product_wrong_token")
cart_data = combine_case_data(test_data, "test_add_product_wrong_cart_id")


# cart_id_test = combine_case_data(test_data, "test_add_product_wrong_input")


@allure.step("前置步骤 ==> 制造过期token")
def generate_expired_token():
    with allure.step("有效用户登录成功，获取token"):
        result = user_center.login_user(COMMON_CONFIG['base_username'], COMMON_CONFIG['base_password'])
        if result.result.get('token'):
            token = result.result.get('token')
        else:
            return "用户{} 登录失败".format(COMMON_CONFIG['base_username'])
    with allure.step("用户退出登录，token: [{}] 过期".format(token)):
        result = user_center.logout_user(token)
        if result.success:
            with allure.step("成功退出登录"):
                logger.info("用户退出登录, token [{}]".format(token))
        else:
            with allure.step("退出失败,请检查原因"):
                return "用户{} 退出登录失败".format(COMMON_CONFIG['base_username'])
    return token


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("交易中心-点餐收银")
class TestCartValidation:
    @allure.story("交易中心-添加购物车接口")
    @pytest.mark.smoke
    @pytest.mark.parametrize("token, items, expect_result, expect_msg, expect_code, title",
                             in_data)
    def test_add_product_wrong_token(self, get_cart_success, token, items, expect_result, expect_msg, expect_code,
                                     title):
        """
        输入错误token，需要获取到正确的cartID等信息
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        expired_token = generate_expired_token()
        if not token:  # 输入token为空，则代表需要生成过期token
            with allure.step("传入过期token: [{}]".format(expired_token)):
                token = expired_token
        else:
            with allure.step("传入非法token: [{}]".format(token)):
                logger.debug("传入非法token: [{}]".format(token))
        with allure.step("获取购物车信息:"):
            active_token, cart_id, cart_result = get_cart_success
            with allure.step("当前用户是[{}], 购物车ID是[{}]".format(COMMON_CONFIG['base_username'], cart_id)):
                logger.info("当前用户是[{}], 购物车ID是[{}]".format(COMMON_CONFIG['base_username'], cart_id))
        with allure.step("有效token是: [{}], 测试token是: [{}]".format(active_token, token)):
            logger.info("有效token是: [{}], 测试token是: [{}]".format(active_token, token))
        with allure.step("添加商品到购物车，添加商品信息为：{}".format(items)):
            result = cart_operation.add_cart(token, cart_id, items)
        with allure.step("验证接口返回结果是否符合预期"):
            with allure.step(
                    "断言调用添加商品接口是否成功：期望值[{}], 实际值[{}]".format(expect_result, result.success)):
                assert result.success == expect_result, result.error
            with allure.step("断言接口返回码：期望值[{}], 实际值[{}]".format(expect_code, result.code)):
                assert result.code == expect_code
            with allure.step("断言接口返回消息：期望值[{}], 实际值[{}]".format(expect_msg, result.msg)):
                assert result.msg in expect_msg
        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-添加购物车接口")
    @allure.issue("https://www.teambition.com/task/65800242fbca1cca3321dbea")
    @pytest.mark.smoke
    @pytest.mark.parametrize("cart_id, items, expect_result, expect_msg, expect_code, title",
                             cart_data)
    def test_add_product_wrong_cart_id(self, get_cart_success, cart_id, items, expect_result, expect_msg, expect_code,
                                     title):
        """
        输入错误的cartid，需要登录成功的token
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        with allure.step("传入错误的购物车ID: [{}]".format(cart_id)):
            logger.debug("传入错误的购物车ID: [{}]".format(cart_id))
        with allure.step("获取购物车信息:"):
            active_token, active_cart_id, cart_result = get_cart_success
            with allure.step("当前用户是[{}], 对应的购物车ID是[{}]".format(COMMON_CONFIG['base_username'], active_cart_id)):
                logger.info("当前用户是[{}], 对应的购物车ID是[{}]".format(COMMON_CONFIG['base_username'], active_cart_id))
        with allure.step("有效的购物车ID是: [{}], 测试购物车ID是: [{}]".format(active_cart_id, cart_id)):
            logger.info("有效token是: [{}], 测试token是: [{}]".format(active_cart_id, cart_id))
        with allure.step("添加商品到购物车，添加商品信息为：{}".format(items)):
            result = cart_operation.add_cart(active_token, cart_id, items)
        with allure.step("验证接口返回结果是否符合预期"):
            with allure.step(
                    "断言调用添加商品接口是否成功：期望值[{}], 实际值[{}]".format(expect_result, result.success)):
                assert result.success == expect_result, result.error
            with allure.step("断言接口返回码：期望值[{}], 实际值[{}]".format(expect_code, result.code)):
                assert result.code == expect_code
            with allure.step("断言接口返回消息：期望值[{}], 实际值[{}]".format(expect_msg, result.msg)):
                assert result.msg in expect_msg
        logger.info("==========用例执行结束=========")


if __name__ == "__main__":
    # pytest.main(['-v -s test_cart_validation::test_add_product_wrong_token'])
    pytest.main(['-v -s test_cart_validation.py'])

    # os.system(r'allure generate ./output/result -o ./output/html --clean')
    # os.system(r"allure serve ./output/result")
