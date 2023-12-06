import requests
from Libraries import COMMON_CONFIG
from Libraries.api.rest_client import RestClient


api_root_url = COMMON_CONFIG["host"]
class User(RestClient):
    def __init__(self, api_root_url):
        super(User, self).__init__(api_root_url)
        # self.root_url = COMMON_COFIG.get("host")
        # self.base_username = COMMON_COFIG.get("base_username")
        # self.base_password = COMMON_COFIG.get("base_password")

    def login(self, **kwargs):
        return self.post("/Pad/v3/Account/CheckLoginByPwd", **kwargs)

    def logout(self, **kwargs):
        #need setup to get token
        return self.post("/Pad/v3/Account/LoginOut", **kwargs)
    def change_pwd(self, **kwargs):
        #need setup to get token
        return self.post("/Pad/v3/Account/ChangePassword", **kwargs)

    def get_ICcard(self, **kwargs):
        #need setup to get login token
        return self.post("/product/v1/Delivery/DeliveryOrderPad", **kwargs)




user = User(api_root_url)