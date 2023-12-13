#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/12/6
# @Author : 连莲


from danta_common import COMMON_CONFIG
from Libraries.request_core.rest_client import RestClient

api_root_url = COMMON_CONFIG["host"]


class Store(RestClient):
    def __init__(self, api_root_url):
        super(Store, self).__init__(api_root_url)

    def get_base(self, **kwargs):
        return self.post("/Pad/v3/Account/GetBase", **kwargs)

    # def update_base(self,**kwargs):
    #     return self.post("/Pad/v3/Account/UpdateBase", **kwargs)

    def modify_store(self, **kwargs):
        return self.post("/Pad/v3/Account/ModifyStore", **kwargs)

    def delivery_order_list(self, **kwargs):
        return self.post("/product/v1/Delivery/DeliveryOrderListPad", **kwargs)

    def delivery_order_print(self, **kwargs):
        return self.post("/product/v1/Delivery/DeliveryOrderPrint", **kwargs)

    def delivery_order_pad(self, **kwargs):
        return self.post("/product/v1/Delivery/DeliveryOrderPad", **kwargs)


store = Store(api_root_url)
