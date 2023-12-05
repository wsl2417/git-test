
from ks_mini.request_send.user_account import UserAccountLoginOUt
from ks_mini.testcases.test_user_account import global_token
class TestLoginOut:
    def test_login_out(self):
        UserAccountLoginOUt.account_loginout(global_token)