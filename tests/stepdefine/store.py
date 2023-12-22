from danta_common.api.store import store
import json
from Libraries.other_tools.phase_response import phase


def get_base_info(token):
    payload = json.dumps({
        "token": token
    })
    header = {
        'Content-Type': 'application/json'
    }
    res = store.get_base(data=payload, headers=header)
    # res = requests.request("POST", url, headers=header, data=payload)
    result_object = phase.phase_res(res)
    return result_object


# def update_base_info():
#     pass


def modify_store_info(token, update_data_dict):
    '''
    修改门店信息，token是必填字段，其他可修改的有isCakeClose, isSelfTake, isOpenSend, isWaimaiSelfTake, isWaimaiClose, isWaimaiOpenSend

    input:
        "isClose": 0,
        "isCakeClose": 0,
        "isSelfTake": 0,
        "isOpenSend": 1,
        "isWaimaiSelfTake": 1,
        "isWaimaiClose": 0,
        "isWaimaiOpenSend": 1,
        "token": ""
    return:
        result_object: code, message, result
    '''
    # login = user_center.login()
    # token = "49629d3a386f496ab0661b06aaf03568"
    # update_dict = {"token": token}
    # origin_info = get_base_info(token)
    # if origin_info.result.get(update_key):
    #     update_dict[update_key] = update_value
    # else:
    #     logger.error("更新的字段不存在: {}! 请检查输入参数。".format(update_key))
    # token = data['token']
    payload = json.dumps(update_data_dict)
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = store.modify_store(data=payload, headers=header)
    result_object = phase.phase_res(res)
    return result_object


def get_delivery_list():
    pass


def print_delivery_order():
    pass


def get_delivery_order_pad():
    pass
