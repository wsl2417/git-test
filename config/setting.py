#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Text

def get_curr_path():
    '''
     获取当前根目录
     :return: path
     '''
    curr_path = os.path.dirname(os.path.dirname(__file__))

    # print('12313123', curr_path, end='\n')
    return curr_path

def get_file_full_path(path):
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return get_curr_path() + path




if __name__=="__main__":
    # path = get_curr_path()
    result = get_file_full_path('/tests')
    print('result',result)