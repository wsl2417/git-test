from Libraries.other_tools.result_item import ResultItem


class PhaseResponse():
    # def __init__(self,res):
    #     self.res = res

    def phase_res(self, res):
        result = ResultItem()
        result.success = False
        print('res.json', res.json())
        if res.json()["code"] == 0:
            result.success = True
            result.token = res.json()["result"]["token"]
        else:
            result.error = "接口返回码是[ {} ], 返回信息：{} ".format(res.json()["code"], res.json()["message"])
        result.msg = res.json()["message"]
        result.response = res
        return result


phase = PhaseResponse()
