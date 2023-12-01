'''
跑用例入口文件
执行：python start.py
'''

import os

def run():
    os.system("pytest testcases/tset_user_account.py --alluredir=./output/result_data")
    os.system("allure serve ./output/result_data")

if __name__=='__main__':
    run()