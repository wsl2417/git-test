import os


def get_all_yaml_files(file_path):
    '''
    获取tests下所有yaml用例数据
    :param file_path: 用例工作目录，
    :return: yaml_file_list: 返回所有包含绝对路径的yaml文件列表
    '''
    yaml_file_list = []
    for root, dirs, files in os.walk(file_path):
        for _path in files:
            path = os.path.join(root, _path)
            if 'yaml' in path or 'yml' in path:
                yaml_file_list.append(path)
            else:
                continue
    return yaml_file_list