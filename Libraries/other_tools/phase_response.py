#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/12/6
# @Author : 连莲

from Libraries.other_tools.result_item import ResultItem
from Libraries.log_generator.logger import logger


class PhaseResponse:
    # def __init__(self,res):
    #     self.res = res

    def phase_res(self, res):
        result = ResultItem()
        result.success = False
        logger.debug("request_core result is:".format(res.json()))
        if res.json()["code"] == 0:
            result.success = True
            result.result = res.json()["result"]
        else:
            result.error = logger.info("接口返回码是[ {} ], 返回信息：{} ".format(res.json()["code"], res.json()["message"]))
        result.msg = res.json()["message"]
        # result.response = res
        result.code = res.json()["code"]
        result.result = res.json()["result"]
        return result



phase = PhaseResponse()
