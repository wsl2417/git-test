import pytest
import allure
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.conftest import test_data
from tests.stepdefine import cart_operation

in_data = combine_case_data(test_data, "test_add_product_by_correct_user")


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("交易中心-点餐收银")
class TestCartOperation:

    @allure.story("交易中心-添加购物车接口")
    @pytest.mark.smoke
    @pytest.mark.parametrize("items, expect_result, expect_msg, expect_code, title",
                             in_data)
    def test_add_product_by_correct_user(self, get_cart_success, items, expect_result, expect_msg, expect_code, title):
        """
        该suite用来测试有权限用户添加商品的接口，包括正确的商品信息，空商品信息，不存在的商品信息，{错误库存没校验}
        1.用户登录，获取门店信息（id,收银方式"cashier/reservation"）==> 输出token,storeId
        2.获取购物车信息 ==> cartId, items
        3.添加商品
            3.1 添加商品成功，(需要去商品中心获取商品类目和数量-》在场景测试中做)
            3.2 添加失败
        4.断言接口返回结果
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, cart_id, cart_result = get_cart_success
        with allure.step("获取前购物车列表信息：购物车ID为[{}]".format(cart_id)):
            logger.debug("当前购物车列表信息如下: {}".format(cart_result))
        with allure.step("添加商品到购物车,添加的商品信息为【{}】".format(items)):
            result = cart_operation.add_cart(token, cart_id, items)
            with allure.step("断言调用添加商品接口是否成功：期望值[{}], 实际值[{}]".format(expect_result,result.success)):
                assert result.success == expect_result, result.error
            with allure.step("断言接口返回码：期望值[{}], 实际值[{}]".format(expect_code, result.code)):
                assert result.code == expect_code
            with allure.step("断言接口返回消息：期望值[{}], 实际值[{}]".format(expect_msg, result.msg)):
                assert result.msg in expect_msg
        logger.info("==========用例执行结束=========")
