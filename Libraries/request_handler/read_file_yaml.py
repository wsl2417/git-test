import os
import logging

import yaml
class GetDataYaml:
    def read_file_yaml(path):
        current_dir = os.path.dirname(os.path.abspath('data'))#获取当前路径
        print('###DEBUG#####',current_dir)
        # logging.log('DEBUG',current_dir)

        # parent_dir = ("/".join(current_dir.split("/")[:-1]))
        parent_dir = ("/".join(current_dir.split("/")))

        file_path = parent_dir + path
        if not os.path.exists(file_path):
            print(f"文件 '{file_path}' 不存在")
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            conf = yaml.load(f.read(), Loader=yaml.FullLoader)
            print(conf)
            return conf






