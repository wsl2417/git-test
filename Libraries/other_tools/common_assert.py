import allure


def common_assert(result_object, **kwargs):
    """
    对测试用例返回的的结果对象进行断言
    : params
    result_object: 接口返回的结果对象包括：
    ** result_object.success: （bool型）接口返回结果成功与否
    ** result_object.result: (dict) 接口返回的数据体
    ** result_object.code: (int) 接口返回的code
    ** result_object.msg: (string) 接口返回的消息
    """
    expect_result = dict(**kwargs).get('expect_result', None)
    expect_code = dict(**kwargs).get('expect_code', None)
    expect_msg = dict(**kwargs).get('expect_msg', None)
    expect_data = dict(**kwargs).get('expect_data', None)
    if expect_result is not None:
        with allure.step("断言接口是否成功：期望值[{}], 实际值[{}]".format(expect_result, result_object.success)):
            assert result_object.success == expect_result, result_object.error
    if expect_msg is not None:
        with allure.step("断言接口返回消息：期望值[{}], 实际值[{}]".format(expect_msg, result_object.msg)):
            assert result_object.msg in expect_msg
    if expect_code is not None:
        with allure.step("断言接口返回码：期望值[{}], 实际值[{}]".format(expect_code, result_object.code)):
            assert result_object.code == expect_code

    # # 目前用在添加购物车后，查询购物车信息符合预期
    # if expect_data:
    #     with allure.step("断言接口返回消息：期望值[{}], 实际值[{}]".format(expect_data, result_object.result)):
    #         assert expect_data in result_object.result
