import json
from danta_common.api.trading_center.cart import cart
from tests.stepdefine.phase_response import phase


def add_cart(token, cartId, items):
    payload = json.dumps({
        "token": token,
        "cartId": cartId,
        "items": items
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = cart.add_cart(data=payload, headers=header)
    result_object = phase.phase_res(res)
    return result_object
