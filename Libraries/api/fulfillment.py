from Libraries import COMMON_CONFIG
from Libraries.api.rest_client import RestClient

api_root_url = COMMON_CONFIG["host"]


class Fulfillment(RestClient):
    def __init__(self, api_root_url):
        super(Fulfillment, self).__init__(api_root_url)

    def call_delivery(self, **kwargs):
        return self.post("/casamiel/api/fulfillment/order/delivery/callDelivery", **kwargs)

    def cancel_call_delivery(self,**kwargs):
        return self.post("/casamiel/api/fulfillment/order/delivery/cancelCallDelivery", **kwargs)

    def get_delivery_service_provider(self,**kwargs):
        return self.post("/casamiel/api/fulfillment/order/delivery/getDeliveryServiceProvider", **kwargs)

    def order_pickup(self,**kwargs):
        return self.post("/casamiel/api/fulfillment/redemption/order/pickup", **kwargs)



fulfillment = Fulfillment()