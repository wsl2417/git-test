import os


import yaml
class GetDataYaml:
    def read_file_yaml(path):
        current_dir = os.path.dirname(os.path.abspath('data'))#获取当前路径



        parent_dir = ("/".join(current_dir.split("/")[:-1]))
                      # + '/data')

        file_path = parent_dir + path
        if not os.path.exists(file_path):
            print(f"文件 '{file_path}' 不存在")
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            conf = yaml.load(f.read(), Loader=yaml.FullLoader)
            print(conf)
            return conf






