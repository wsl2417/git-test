import json

from danta_common.api.pendingorder import pending
from Libraries.other_tools.phase_response import phase



def pending_order_list(token, storeId):
    payload = json.dumps({
        "token": token,
        "storeId": storeId
    })
    header = {
        'Content-Type': 'application/json'
    }
    # user = User()
    res = pending.get_order_list(data=payload, headers=header)
    # res = requests.request("POST", url, headers=header, data=payload)
    result_object = phase.phase_res(res.text)

    return result_object



