import pytest
import allure
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.conftest import test_data
from tests.stepdefine import cart_operation
from tests.testcases.trade_center.conftest import (add_cart_success, prepare_cart_items, compare_cart_items,
                                                   init_items_num)
from Libraries.other_tools.common_assert import common_assert

function_list = ['test_add_product_by_correct_user', 'test_change_cart_by_correct_user',
                 'test_increase_cart_by_correct_user', 'test_decrease_cart_by_correct_user',
                 'test_clear_cart_by_correct_user', 'test_remove_cart_by_correct_user',
                 'test_exchange_cart_by_correct_user', 'test_get_cart_info_by_correct_user']

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
@allure.step("获取当前购物车信息")
def print_curr_cart_info(cart_id, curr_cart_result):
    with allure.step("当前购物车对应的门店ID: {}".format(curr_cart_result.get('storeId'))):
        logger.info("当前购物车对应的门店ID: {}".format(curr_cart_result.get('storeId')))
    with allure.step("当前购物车ID为[{}], 购物车商品信息列表为[{}]".format(cart_id, curr_cart_result)):
        logger.debug("当前购物车列表信息如下: {}".format(curr_cart_result.get('items', [])))


@allure.step("查询最新购物车信息列表")
def get_latest_cart_list(token, store_id, scene='cashier'):
    curr_cart_result_object = cart_operation.get_cart_info(token, store_id, scene)
    common_assert(curr_cart_result_object, expect_result=True)
    with allure.step("当前购物车商品列表: {}".format(curr_cart_result_object.result)):
        return curr_cart_result_object.result


@allure.step("购物车商品更新信息准确")
def verify_cart_list_as_expected(curr_cart_item_list, update_items):
    """
    根据更新的商品信息，验证购物车中商品信息是否更新正确
    """
    # return all(item['itemNum'] == curr_item['itemNum'] if item['skuCode'] == curr_item['skuCode']
    #            for item in update_items for curr_item in curr_cart_item_list)
    if (not curr_cart_item_list) and (not update_items):
        return True
    else:
        for item in update_items:
            for curr_item in curr_cart_item_list:
                if item['skuCode'] == curr_item['skuCode']:
                    if item['itemNum'] == curr_item['itemNum']:
                        logger.info("商品[{}]数量更新正确".format(item['skuCode']))
                        return True
                    else:
                        logger.info("商品[{}]数量更新错误".format(item['skuCode']))
                        return False


@allure.step("验证指定商品不在购物车列表")
def check_items_should_not_in_cart(current_cart_item_list, remove_or_exchange_items):
    """
    验证最新购物车列表中被替换，删除，清空的商品信息正确
    """
    if_items_existed, intersection_sku_list = compare_cart_items(current_cart_item_list,
                                                                 remove_or_exchange_items)
    if if_items_existed:
        with allure.step("购物车中存在被删除或替换的商品，商品列表为：{}".format(intersection_sku_list)):
            logger.info("购物车中存在被删除或替换的商品，商品列表为：{}".format(intersection_sku_list))
            return False
    else:
        with allure.step("购物车中不存在被删除或替换的商品，商品列表为：{}".format(intersection_sku_list)):
            logger.info("购物车中不存在被删除或替换的商品，商品列表为：{}".format(intersection_sku_list))
            return True


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
        token, cart_id, curr_cart_result = get_cart_success
        store_id = curr_cart_result.get('storeId')
        print_curr_cart_info(cart_id, curr_cart_result)
        with allure.step("购物车数据准备"):
            with allure.step("删除购物车中待更新的商品信息"):
                prepare_cart_items(token, cart_id, curr_cart_result, items)
        # 查询初始化后的购物车
        latest_items_list_1 = get_latest_cart_list(token, store_id)
        with allure.step("添加商品到购物车"):
            with allure.step("添加的商品信息为【{}】".format(items)):
                result = cart_operation.add_cart(token, cart_id, items)
            with allure.step("断言接口测试结果"):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        with allure.step("查询变更后的结果"):
            latest_items_list_2 = get_latest_cart_list(token, store_id)
            with allure.step("当前购物车商品列表信息正确"):
                if expect_result and len(items):
                    with allure.step("如果是添加成功的用例，则对比添加的商品信息在购物车中信息正确"):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'], items)
                        assert if_cart_updated is True
                else:
                    with allure.step("如果是添加失败的用例，则对比购物车信息等于初始化的购物车信息"):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'],
                                                                       latest_items_list_1['items'])
                        assert if_cart_updated is True
        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-调整购物车商品数量接口")
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
        token, cart_id, curr_cart_result = get_cart_success
        store_id = curr_cart_result.get('storeId')
        print_curr_cart_info(cart_id, curr_cart_result)
        with allure.step("购物车数据准备"):
            with allure.step("删除购物车中待更新的商品信息"):
                prepare_cart_items(token, cart_id, curr_cart_result, items)
            # 如果是成功的正向用例，则添加初始化商品信息
            if expect_result:
                with allure.step("添加待初始化的待变更商品信息到购物车"):
                    init_items = init_items_num(items, 1)
                    with allure.step("添加初始化商品：{}".format(init_items)):
                        init_result = cart_operation.add_cart(token, cart_id, init_items)
                        common_assert(init_result, expect_result=True)
        # 查询添加后的购物车
        latest_items_list_1 = get_latest_cart_list(token, store_id)
        if expect_result:
            with allure.step("当前购物车商品列表信息正确"):
                # 验证购物车信息符合预期
                if_cart_updated = verify_cart_list_as_expected(latest_items_list_1['items'], init_items)
                assert if_cart_updated is True
        with allure.step("调整购物车商品数量"):
            with allure.step("待调整的商品信息为: {}".format(items)):
                result = cart_operation.change_cart(token, cart_id, items)
            with allure.step("断言接口测试结果"):
                # common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
                # TODO 不存在的商品类目返回的message不准确，暂时不断言message
                common_assert(result, expect_result=expect_result, expect_code=expect_code)
        with allure.step("查询调整后的结果"):
            latest_items_list_2 = get_latest_cart_list(token, store_id)
            with allure.step("当前购物车商品列表信息正确"):
                if expect_result:
                    with allure.step("如果是成功的用例，则对比更新的商品信息在购物车中信息正确"):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'], items)
                        assert if_cart_updated is True
                else:
                    with allure.step("如果是失败的用例，则对比购物车信息等于初始化的购物车信息"):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'],
                                                                       latest_items_list_1['items'])
                        assert if_cart_updated is True
            # 判断变更结果生效，如果result.success则判断变更后购物车中商品和更新的类目一致，否则判断购物车中商品和更新的类目不一致
        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-增加购物车商品数量接口")
    # @allure.issue(url="https://www.teambition.com/project/623944d5cc091382e72ad9ed/bug/task/658405c504411144bd5299c0",
    #               name="变更购物车内没有的商品返回结果错误")
    @pytest.mark.smoke
    @pytest.mark.parametrize("items, expect_result, expect_msg, expect_code, title",
                             data_2, ids=ids_2)
    def test_increase_cart_by_correct_user(self, get_cart_success, items, expect_result, expect_msg, expect_code,
                                           title):
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, cart_id, curr_cart_result = get_cart_success
        store_id = curr_cart_result.get('storeId')
        print_curr_cart_info(cart_id, curr_cart_result)
        with allure.step("购物车数据准备"):
            with allure.step("删除购物车中待更新的商品信息"):
                prepare_cart_items(token, cart_id, curr_cart_result, items)
            if expect_result:
                with allure.step("添加待初始化的待变更商品信息到购物车"):
                    init_items = init_items_num(items, 1)
                    with allure.step("添加初始化商品：{}".format(init_items)):
                        add_cart_success(token, cart_id, init_items)
            # 查询添加后的购物车
        latest_items_list_1 = get_latest_cart_list(token, store_id)
        with allure.step("当前购物车商品列表信息正确"):
            # 验证购物车信息符合预期
            if expect_result:
                if_cart_updated = verify_cart_list_as_expected(latest_items_list_1['items'], init_items)
                assert if_cart_updated is True
            else:
                with allure.step("购物车列表没有更新"):
                    logger.info("购物车列表没有更新")
        with allure.step("增加购物车商品数量"):
            with allure.step("增加的商品信息为: {}".format(items)):
                result = cart_operation.increase_cart_item(token, cart_id, items)
            with allure.step("断言接口测试结果"):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        latest_items_list_2 = get_latest_cart_list(token, store_id)
        with allure.step("当前购物车商品列表信息正确"):
            if expect_result:
                with allure.step("如果是更新成功的用例，则对比更新的商品信息在购物车中信息正确"):
                    if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'], items)
                    assert if_cart_updated is True
            else:
                with allure.step("如果是更新失败的用例，则对比购物车信息等于初始化的购物车信息"):
                    if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'],
                                                                   latest_items_list_1['items'])
                    assert if_cart_updated is True

        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-减少购物车商品数量接口")
    @pytest.mark.smoke
    @allure.issue("https://www.teambition.com/task/6589209b9a62a177eb654c01", "商品skuCode未做校验")
    @pytest.mark.parametrize("items, expect_result, expect_msg, expect_code, title",
                             data_3, ids=ids_3)
    def test_decrease_cart_by_correct_user(self, get_cart_success, items, expect_result, expect_msg, expect_code,
                                           title):
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, cart_id, curr_cart_result = get_cart_success
        store_id = curr_cart_result.get('storeId')
        print_curr_cart_info(cart_id, curr_cart_result)
        with allure.step("购物车数据准备"):
            with allure.step("删除购物车中待更新的商品信息 {}".format(items)):
                prepare_cart_items(token, cart_id, curr_cart_result, items)
                latest_items_list_0 = get_latest_cart_list(token, store_id)
            # 如果测试商品的skuCode在商品类目中，则添加初始化商品信息，这里为了测试减少商品，初始数量设置为2
            if expect_result:
                with allure.step("添加待初始化的待变更商品信息到购物车"):
                    init_items = init_items_num(items, 2)
                    with allure.step("添加初始化商品：{}".format(init_items)):
                        if_add_success = add_cart_success(token, cart_id, init_items)
        # 查询添加后的购物车
        latest_items_list_1 = get_latest_cart_list(token, store_id)
        with allure.step("当前购物车商品列表信息正确"):
            # 验证购物车信息符合预期
            if expect_result:
                if_cart_updated = verify_cart_list_as_expected(latest_items_list_1['items'], init_items)
                assert if_cart_updated is True
            else:
                with allure.step("购物车列表没有更新"):
                    logger.info("购物车列表没有更新")
        with allure.step("减少购物车商品数量"):
            with allure.step("减少的商品信息为: {}".format(items)):
                result = cart_operation.decrease_cart_item(token, cart_id, items)
            with allure.step("断言接口测试结果"):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        latest_items_list_2 = get_latest_cart_list(token, store_id)
        with allure.step("当前购物车商品列表信息正确"):
            if expect_result:
                with allure.step("如果是更新成功的用例，则对比删除的商品信息在购物车中信息正确"):
                    if_cart_updated = verify_cart_list_as_expected(latest_items_list_2.get('items'), items)
                    assert if_cart_updated is True
            else:
                with allure.step("如果是更新失败的用例，则对比购物车信息等于初始化的购物车信息"):
                    if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'],
                                                                   latest_items_list_1['items'])
                    assert if_cart_updated is True

        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-清空购物车商品接口")
    @pytest.mark.normal
    @pytest.mark.parametrize("cart_id, expect_result, expect_msg, expect_code, title",
                             data_4, ids=ids_4)
    def test_clear_cart_by_correct_user(self, get_cart_success, cart_id, expect_result, expect_msg, expect_code,
                                        title):
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, active_cart_id, curr_cart_result = get_cart_success
        store_id = curr_cart_result.get('storeId')
        print_curr_cart_info(active_cart_id, curr_cart_result)
        with allure.step("购物车数据准备"):
            if expect_result:
                with allure.step("添加待初始化的待变更商品信息到购物车"):
                    init_items = init_items_num([{'skuCode': '928', 'itemNum': 0}], 2)
                    with allure.step("添加初始化商品：{}".format(init_items)):
                        if_add_success = add_cart_success(token, active_cart_id, init_items)
        # 查询当前购物车信息
        latest_items_list_1 = get_latest_cart_list(token, store_id)
        with allure.step("清空购物车"):
            with allure.step("清空购物车传入的购物车ID为：{}".format(cart_id)):
                result = cart_operation.clear_cart(token, cart_id)
            with allure.step("断言接口测试结果"):
                # common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
                common_assert(result, expect_result=expect_result, expect_code=expect_code)
        with allure.step("查询变更后的结果"):
            latest_items_list_2 = get_latest_cart_list(token, store_id)
            with allure.step("当前购物车商品列表信息正确"):
                if expect_result:
                    with allure.step("如果是清空成功的用例，则对比购物车信息为空"):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'], [])
                        assert if_cart_updated is True
                else:
                    with allure.step("如果是更新失败的用例，则对比购物车信息等于初始化的购物车信息"):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'],
                                                                       latest_items_list_1['items'])
                        assert if_cart_updated is True

        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-移除指定商品接口")
    @pytest.mark.smoke
    @allure.issue("https://www.teambition.com/project/623944d5cc091382e72ad9ed/bug/task/658bcabf7134313decfc1e80",
                  "关键字段没有加限制")
    @pytest.mark.parametrize("items, expect_result, expect_msg, expect_code, title",
                             data_5, ids=ids_5)
    def test_remove_cart_by_correct_user(self, get_cart_success, items, expect_result, expect_msg, expect_code,
                                         title):
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, cart_id, curr_cart_result = get_cart_success
        store_id = curr_cart_result.get('storeId')
        print_curr_cart_info(cart_id, curr_cart_result)
        if expect_result:
            with allure.step("购物车数据准备"):
                with allure.step("添加待初始化的待变更商品信息到购物车"):
                    init_items = init_items_num(items, 2)
                    with allure.step("添加初始化商品：{}".format(init_items)):
                        if_add_success = add_cart_success(token, cart_id, init_items)
        # 查询当前购物车信息
        latest_items_list_1 = get_latest_cart_list(token, store_id)
        with allure.step("移除指定商品"):
            with allure.step("移除的商品信息为: {}".format(items)):
                result = cart_operation.remove_cart(token, cart_id, items)
            with allure.step("断言接口测试结果"):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)

        with allure.step("查询变更后的结果"):
            latest_items_list_2 = get_latest_cart_list(token, store_id)
            with allure.step("当前购物车商品列表信息正确"):
                if expect_result:
                    with allure.step("移除成功，购物车中不应该存在被移除的商品"):
                        if_cart_updated = check_items_should_not_in_cart(latest_items_list_2['items'], items)
                        assert if_cart_updated is True
                else:
                    with allure.step("移除失败，购物车信息保持不变"):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'],
                                                                       latest_items_list_1['items'])
                        assert if_cart_updated is True

        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-更换商品规格接口")
    @pytest.mark.smoke
    @allure.issue("https://www.teambition.com/project/623944d5cc091382e72ad9ed/bug/task/658bf7bbd63d8eb240aef39a",
                  "[更换购物车商品API]oldItem没有校验")
    @allure.issue("https://www.teambition.com/project/623944d5cc091382e72ad9ed/bug/task/658c01e477241bb03bff434c",
                  "[更换购物车商品API]newItem传入不存在的skuCode，oldItem会被移除")
    @pytest.mark.parametrize("old_items, new_items, expect_result, expect_msg, expect_code, title",
                             data_6, ids=ids_6)
    def test_exchange_cart_by_correct_user(self, get_cart_success, old_items, new_items,
                                           expect_result, expect_msg, expect_code, title):
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, cart_id, curr_cart_result = get_cart_success
        store_id = curr_cart_result.get('storeId')
        print_curr_cart_info(cart_id, curr_cart_result)
        with allure.step('变更购物车商品规格或数目'):
            with allure.step('旧的商品信息：{}, 新的商品信息：{}'.format(old_items, new_items)):
                result = cart_operation.exchange_cart(token, cart_id, old_items, new_items)
            with allure.step('断言接口测试结果'):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)
        with allure.step('查询最新购物车列表'):
            latest_items_list_2 = get_latest_cart_list(token, store_id)
            with allure.step('当前购物车商品列表信息正确'):
                if expect_result:
                    with allure.step('商品更换成功，购物车中商品信息已更新'):
                        # if_cart_updated = check_items_should_not_in_cart(latest_items_list_2['items'], old_items)
                        # assert if_cart_updated is True
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'], new_items)
                        assert if_cart_updated is True
                else:
                    with allure.step('变更失败，购物车信息保持不变'):
                        if_cart_updated = verify_cart_list_as_expected(latest_items_list_2['items'],
                                                                       curr_cart_result['items'])
                        assert if_cart_updated is True

        logger.info("==========用例执行结束=========")

    @allure.story("交易中心-获取购物车信息接口")
    @pytest.mark.smoke
    # @allure.issue("https://www.teambition.com/project/623944d5cc091382e72ad9ed/bug/task/658bf7bbd63d8eb240aef39a",
    # "[更换购物车商品API]oldItem没有校验")
    @pytest.mark.parametrize("scene, expect_result, expect_msg, expect_code, title", data_7, ids=ids_7)
    def test_get_cart_info_by_correct_user(self, get_store_success, scene, expect_result, expect_msg, expect_code,
                                           title):
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        token, active_store_id = get_store_success
        with allure.step("当前用户对应的门店ID是[{}]".format( active_store_id)):
            logger.info("当前用户对应的门店ID是[{}]".format(active_store_id))
        with allure.step('获取购物车信息列表'):
            result = cart_operation.get_cart_info(token, active_store_id, scene)
            with allure.step('断言接口测试结果'):
                common_assert(result, expect_result=expect_result, expect_code=expect_code, expect_msg=expect_msg)

        logger.info("==========用例执行结束=========")


if __name__ == "__main__":
    pytest.main(['-s', '-v', 'test_cart_operation.py::test_decrease_cart_by_correct_user'])
