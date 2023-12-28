#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/12/13
# @Author : 连莲


from danta_common import COMMON_CONFIG
from Libraries.request_core.rest_client import RestClient

api_root_url = COMMON_CONFIG["host"]


class Cart(RestClient):
    """
    交易中心购物车操作接口
    """

    def __init__(self, api_root_url):
        super(Cart, self).__init__(api_root_url)

    def add_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/addCart", **kwargs)

    def get_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/getCart", **kwargs)

    def change_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/changeCart", **kwargs)

    def clear_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/clearCart", **kwargs)

    def decrease_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/decreaseCart", **kwargs)

    def exchange_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/exchangeCart", **kwargs)

    def increase_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/increaseCart", **kwargs)

    def remove_cart(self, **kwargs):
        return self.post("/casamiel/api/trade/seller/cart/removeCart", **kwargs)


cart = Cart(api_root_url)
