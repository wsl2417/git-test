import pytest
import allure
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.conftest import test_data
from tests.stepdefine import cart_operation
from tests.stepdefine import user_center
from danta_common import COMMON_CONFIG
from Libraries.other_tools.common_assert import common_assert

function_list = ['test_add_product_wrong_token', 'test_add_product_wrong_cart_id', 'test_change_cart_wrong_token',
                 'test_change_cart_wrong_cart_id']
for index, elem in enumerate(function_list):
    data, id = combine_case_data(test_data, elem)
    exec('data_{index}, ids_{index} = {data}, {id}'.format(index=index, data=data, id=id))


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


@allure.step("查询最新购物车信息列表")
def get_latest_cart_list(token, store_id, scene='cashier'):
    curr_cart_result_object = cart_operation.get_cart_info(token, store_id, scene)
    common_assert(curr_cart_result_object, expect_result=True)
    with allure.step("当前购物车商品列表: {}".format(curr_cart_result_object.result)):
        return curr_cart_result_object.result



@allure.severity(allure.severity_level.NORMAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("交易中心-点餐收银")
class TestCartValidation:
    @allure.story("交易中心-添加购物车接口")
    @pytest.mark.smoke
    @pytest.mark.parametrize("token, items, expect_result, expect_msg, expect_code, title",
                             data_0, ids=ids_0)
    def test_add_product_wrong_token(self, get_cart_success, token, items, expect_result, expect_msg, expect_code,
                                     title):
        """
        输入错误token，需要获取到正确的cartID等信息
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        if not token:  # 输入token为空，则代表需要生成过期token
            token = generate_expired_token()
            with allure.step("传入过期token: [{}]".format(token)):
                logger.info("传入过期token: [{}]".format(token))
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
            common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-添加购物车接口")
    @allure.issue("https://www.teambition.com/task/65800242fbca1cca3321dbea")
    @pytest.mark.smoke
    @pytest.mark.parametrize("cart_id, items, expect_result, expect_msg, expect_code, title",
                             data_1, ids=ids_1)
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
            with allure.step(
                    "当前用户是[{}], 对应的购物车ID是[{}]".format(COMMON_CONFIG['base_username'], active_cart_id)):
                logger.info(
                    "当前用户是[{}], 对应的购物车ID是[{}]".format(COMMON_CONFIG['base_username'], active_cart_id))
        with allure.step("有效的购物车ID是: [{}], 测试购物车ID是: [{}]".format(active_cart_id, cart_id)):
            logger.info("有效token是: [{}], 测试token是: [{}]".format(active_cart_id, cart_id))
        with allure.step("添加商品到购物车，添加商品信息为：{}".format(items)):
            result = cart_operation.add_cart(active_token, cart_id, items)
        with allure.step("验证接口返回结果是否符合预期"):
            common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-变更购物车接口")
    @pytest.mark.smoke
    # @pytest.mark.parametrize("case_skip", data_tag_map2, indirect=True)
    @pytest.mark.parametrize("token, items, expect_result, expect_msg, expect_code, title",
                             data_2, ids=ids_2)
    def test_change_cart_wrong_token(self, get_cart_success, token, items, expect_result, expect_msg, expect_code,
                                     title):
        """
        输入错误token，需要获取到正确的cartID等信息
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        if not token:  # 输入token为空，则代表需要生成过期token
            token = generate_expired_token()
            with allure.step("传入过期token: [{}]".format(token)):
                logger.info("传入过期token: [{}]".format(token))
        else:
            with allure.step("传入非法token: [{}]".format(token)):
                logger.debug("传入非法token: [{}]".format(token))
        with allure.step("获取当前购物车信息"):
            active_token, cart_id, curr_cart_result = get_cart_success
            with allure.step("当前购物车对应的门店ID: {}"):
                store_id = curr_cart_result.get('storeId')
            with allure.step("当前购物车ID为[{}], 门店ID为[{}],购物车商品信息列表为[{}]".format(cart_id, store_id, curr_cart_result)):
                logger.debug("当前购物车列表信息如下: {}".format(curr_cart_result.get('items', [])))
        with allure.step("传递无效token,发起变更购物车商品信息"):
            with allure.step("变更商品信息为: {}".format(items)):
                result = cart_operation.change_cart(token, cart_id, items)
            with allure.step("断言接口测试结果"):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        with allure.step("查询变更后的结果"):
            get_latest_cart_list(active_token, store_id)

    @allure.story("交易中心-变更购物车接口")
    @pytest.mark.smoke
    # @pytest.mark.parametrize("case_skip", data_tag_map2, indirect=True)
    @pytest.mark.parametrize("cart_id, items, expect_result, expect_msg, expect_code, title",
                             data_3, ids=ids_3)
    def test_change_cart_wrong_cart_id(self, get_cart_success, cart_id, items, expect_result, expect_msg, expect_code,
                                       title):
        """
        输入错误的购物车ID,请求变更购物车失败
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        with allure.step("传入错误的购物车ID: [{}]".format(cart_id)):
            logger.debug("传入错误的购物车ID: [{}]".format(cart_id))
        with allure.step("获取购物车信息"):
            active_token, active_cart_id, cart_result = get_cart_success
            with allure.step(
                    "当前用户是[{}], 对应的购物车ID是[{}]".format(COMMON_CONFIG['base_username'], active_cart_id)):
                logger.info(
                    "当前用户是[{}], 对应的购物车ID是[{}]".format(COMMON_CONFIG['base_username'], active_cart_id))
        with allure.step("有效的购物车ID是: [{}], 测试购物车ID是: [{}]".format(active_cart_id, cart_id)):
            logger.info("有效token是: [{}], 测试token是: [{}]".format(active_cart_id, cart_id))
        with allure.step("传递无效cartId, 请求变更购物车失败"):
            with allure.step("变更商品信息为: {}".format(items)):
                result = cart_operation.change_cart(active_token, cart_id, items)
            with allure.step("断言接口测试结果"):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        logger.info("==========用例执行结束=========")


if __name__ == "__main__":
    # pytest.main(['-v -s test_cart_validation::test_add_product_wrong_token'])
    pytest.main(['-v -s test_cart_validation.py'])

    # os.system(r'allure generate ./output/result -o ./output/html --clean')
    # os.system(r"allure serve ./output/result")
