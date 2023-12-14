#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/12/13
# @Author : 连莲


from danta_common import COMMON_CONFIG
from Libraries.request_core.rest_client import RestClient

api_root_url = COMMON_CONFIG["host"]


class Goods(RestClient):
    """
    商品中心所有接口
    """

    def __init__(self, api_root_url):
        super(Goods, self).__init__(api_root_url)

    def get_goods_detail(self, **kwargs):
        # 获取商品详细信息
        return self.post("/Pad/v3/Goods/GetDetails", **kwargs)

    def get_goods_spu(self, **kwargs):
        # 按门店和商品ID获取商品SPU信息
        return self.post("/Pad/v3/Goods/GetSpu", **kwargs)

    def get_goods_category(self, **kwargs):
        # 获取商品类目ID
        return self.post("/Pad/v3/Goods/GetCategory", **kwargs)

    def get_spu_list_by_page(self, **kwargs):
        # 按商品分类，门店ID分页显示商品SPU列表
        return self.post("/Pad/v3/Goods/GetSpuList", **kwargs)


goods = Goods(api_root_url)