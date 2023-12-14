#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/12/13
# @Author : 连莲


from danta_common import COMMON_CONFIG
from Libraries.request_core.rest_client import RestClient

api_root_url = COMMON_CONFIG["host"]


class Order(RestClient):
    def __init__(self, api_root_url):
        super(Order, self).__init__(api_root_url)

    def get_detail(self, **kwargs):
        return self.post("/casamiel/api/trade/order/getDetail", **kwargs)

    def get_pending_print_orders(self, **kwargs):
        return self.post("/casamiel/api/trade/order/getPendingPrintOrders", **kwargs)

    def manual_cancel(self, **kwargs):
        return self.post("/casamiel/api/trade/order/manualCancel", **kwargs)

    def manual_complete(self, **kwargs):
        return self.post("/casamiel/api/trade/order/manualComplete", **kwargs)

    def search_page(self, **kwargs):
        return self.post("/casamiel/api/trade/order/searchPage", **kwargs)

    def notify_get_auto(self, **kwargs):
        return self.post("/casamiel/api/trade/order/notification/getAudio", **kwargs)

    def notify_get_page(self, **kwargs):
        return self.post("/casamiel/api/trade/order/notification/getPage", **kwargs)

    def notify_get_unread_count(self, **kwargs):
        return self.post("/casamiel/api/trade/order/notification/getUnreadCount", **kwargs)

    def notify_update_to_read(self, **kwargs):
        return self.post("/casamiel/api/trade/order/notification/read", **kwargs)

    def get_receipt_info(self, **kwargs):
        return self.post("/casamiel/api/trade/order/receipt/getInfo", **kwargs)

    def print_receipt(self, **kwargs):
        return self.post("/casamiel/api/trade/order/receipt/print", **kwargs)


order = Order(api_root_url)
