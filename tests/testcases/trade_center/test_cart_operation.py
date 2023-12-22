import pytest
import allure
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.conftest import test_data
from tests.stepdefine import cart_operation
from tests.testcases.trade_center.conftest import (add_cart_success, prepare_cart_items, remove_cart_success,
                                                   init_items_num)
from Libraries.other_tools.common_assert import common_assert

function_list = ['test_add_product_by_correct_user', 'test_change_cart_by_correct_user']
for index, elem in enumerate(function_list):
    data, id = combine_case_data(test_data, elem)
    exec('data_{index}, ids_{index} = {data}, {id}'.format(index=index, data=data, id=id))

# @allure.step("前置步骤 ==> 过滤不需要跑的用例")
# @pytest.mark.parametrize("case_skip", [data_tag_map1, data_tag_map2], indirect=True)
# def setup_method(case_skip):
#     case_skip()


# @pytest.fixture(scope="function")
# def change_cart_setup(prepare_cart_items, get_cart_success, add_cart_success, request):
#     """
#     1.调用prepare_cart_items函数，删除购物车中待更新的商品信息
#     2.查询删除后的购物车列表
#     3.添加待更新的商品信息到购物车，默认数量设置为1
#     """
#     logger.info("request.param: {}".format(request.param))

@allure.step("查询最新购物车信息列表")
def get_latest_cart_list(token, store_id, scene='cashier'):
    curr_cart_result_object = cart_operation.get_cart_info(token, store_id, scene)
    common_assert(curr_cart_result_object, expect_result=True)
    with allure.step("当前购物车商品列表: {}".format(curr_cart_result_object.result)):
        return curr_cart_result_object.result


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("交易中心-点餐收银")
class TestCartOperation:

    @allure.story("交易中心-添加购物车接口")
    @pytest.mark.smoke
    # @pytest.mark.parametrize("case_skip", data_tag_map1, indirect=True)
    @pytest.mark.parametrize("items, expect_result, expect_msg, expect_code, title",
                             data_0, ids=ids_0)
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
        # is_run = case_skip
        # if not is_run:
        #     with allure.step("跳过用例：{}".format(title)):
        #         logger.info("")
        logger.info("==========开始执行用例=========")
        token, cart_id, cart_result = get_cart_success
        with allure.step("获取当前购物车列表信息：购物车ID为[{}]".format(cart_id)):
            logger.debug("当前购物车列表信息如下: {}".format(cart_result))
        with allure.step("添加商品到购物车,添加的商品信息为【{}】".format(items)):
            result = cart_operation.add_cart(token, cart_id, items)
        with allure.step("断言接口测试结果"):
            common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-变更购物车接口")
    @allure.issue(url="https://www.teambition.com/project/623944d5cc091382e72ad9ed/bug/task/658405c504411144bd5299c0",
                  name="变更购物车内没有的商品返回结果错误")
    @pytest.mark.smoke
    # @pytest.mark.parametrize("case_skip", data_tag_map2, indirect=True)
    @pytest.mark.parametrize("items, expect_result, expect_msg, expect_code, title",
                             data_1, ids=ids_1)
    def test_change_cart_by_correct_user(self, get_cart_success, items, expect_result, expect_msg,
                                         expect_code, title):
        """
        该suite用来测试有权限用户变更商品的接口，变更包括已存在的商品信息，空商品信息，不存在的商品信息，{错误库存没校验}
        1.用户登录，获取门店信息（id,收银方式"cashier/reservation"），根据前两步获取到的信息去获取购物车信息返回==> token, cartId, items(购物车商品信息）
        3.变更商品
            3.1 变更商品成功（根据用例传入数据，先从现有购物车中删除掉要添加的商品然后再调用添加商品接口添加指定数量的商品，然后再调用该变更接口进行测试）
            3.2 传入空商品信息，返回成功
            3.3.传入不在购物车的商品信息，返回失败
            3.4.传入不存在的商品类目，返回变更失败
        4.断言接口返回结果
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        with allure.step("获取当前购物车信息"):
            token, cart_id, curr_cart_result = get_cart_success
            with allure.step("当前购物车对应的门店ID: {}"):
                store_id = curr_cart_result.get('storeId')
            with allure.step("当前购物车ID为[{}], 门店ID为[{}],购物车商品信息列表为[{}]".format(cart_id, store_id, curr_cart_result)):
                logger.debug("当前购物车列表信息如下: {}".format(curr_cart_result.get('items', [])))
        with allure.step("购物车数据准备: items{}".format(items)):
            with allure.step("删除购物车中待更新的商品信息"):
                prepare_cart_items(token, cart_id, curr_cart_result, items)
            # 如果是成功的正向用例，则添加初始化商品信息
            if expect_result:
                with allure.step("添加待初始化的待变更商品信息到购物车 items{}".format(items)):
                    init_items = init_items_num(items, 1)
                    with allure.step("添加初始化商品：{}, items: {}".format(init_items, items)):
                        init_result = cart_operation.add_cart(token, cart_id, init_items)
                        common_assert(init_result, expect_result=True)
            # 查询添加后的购物车
            latest_cart_list = get_latest_cart_list(token, store_id)
        with allure.step("变更购物车商品信息"):
            with allure.step("变更商品信息为: {}".format(items)):
                result = cart_operation.change_cart(token, cart_id, items)
            with allure.step("断言接口测试结果"):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        with allure.step("查询变更后的结果"):
            get_latest_cart_list(token, store_id)

            # curr_cart_result_object = cart_operation.get_cart_info(token, store_id, 'cashier')
            # with allure.step("购物车变更后结果：{}".format(curr_cart_result_object.result)):
            #     logger.info("购物车变更后结果：{}".format(curr_cart_result_object.result))
            # 判断变更结果生效，如果result.success则判断变更后购物车中商品和更新的类目一致，否则判断购物车中商品和更新的类目不一致

        logger.info("==========用例执行结束=========")
