import allure
import pytest
from Libraries.request_handler.user import User

@allure.severity(allure.severity_level.CRITICAL)
@allure.epic()
def TestUserLogin:
    def test_user_login():
        pass
        #根据输入的yaml：step1.解析用例数据 done
        # step2.封装好reqeust操作 done
        # step3. 配置好用例的setup/teardown ongoing
        # step4. 发送请求并解析结果 TODO
        # step5. 对结果断言以及打印log和封装report信息 todo