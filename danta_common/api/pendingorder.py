from danta_common import COMMON_CONFIG
from Libraries.request_core.rest_client import RestClient

api_root_url = COMMON_CONFIG["host"]


class PendingOrder(RestClient):
    def __init__(self, api_root_url):
        super(PendingOrder, self).__init__(api_root_url)

    def get_order_list(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/pending/getOrderList", **kwargs)


pending_order = PendingOrder(api_root_url)
