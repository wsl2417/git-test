from Libraries.api.store import store
import json
from tests.stepdefine.phase_response import phase


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


def modify_store_info():
    '''
    pre step is get base info
    '''
    pass


def get_delivery_list():
    pass


def print_delivery_order():
    pass


def get_delivery_order_pad():
    pass
