'''
跑用例入口文件
执行：python start.py
'''

import os
import pytest
import allure
# import
def run():
    # os.system("pytest testcases/tset_user_account.py --alluredir=./output/result_data")
    pytest.main(['test_user_account.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
    os.system(r"allure serve ./output/result_data")

if __name__=='__main__':
    run()