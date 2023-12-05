#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
跑用例入口文件
执行：python start.py
'''

import os
import pytest
import allure
# import
def run():
    # current_dir = os.path.dirname(os.path.abspath('data'))  # 获取当前路径
    pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                 '--alluredir', './output/result',"--clean-alluredir"])
    '''
    
    '''
    # os.system(r'allure generate ./output/result -o ./output/html --clean')
    # os.system(r"allure serve ./output/result")

if __name__=='__main__':
    run()