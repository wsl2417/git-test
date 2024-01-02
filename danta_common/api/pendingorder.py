from danta_common import COMMON_CONFIG
from Libraries.request_core.rest_client import RestClient

api_root_url = COMMON_CONFIG["host"]


class PenDingOrder(RestClient):
    def __init__(self, api_root_url):
        super(PenDingOrder, self).__init__(api_root_url)
        # self.base_username = COMMON_COFIG.get("base_username")
        # self.base_password = COMMON_COFIG.get("base_password")

    def get_order_list(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/pending/getOrderList", **kwargs)


pending = PenDingOrder(api_root_url)
