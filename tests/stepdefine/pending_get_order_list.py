import json

from danta_common.api.pendingorder import pending_order
from Libraries.other_tools.phase_response import phase



def pending_order_list(token, storeId):
    payload = json.dumps({
        "token": token,
        "storeId": storeId
    })
    header = {
        'Content-Type': 'application/json'
    }

    res = pending_order.get_order_list(data=payload, headers=header)
    result_object = phase.phase_res(res.text)

    return result_object



