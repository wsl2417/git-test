import os.path

from Libraries.read_data.get_yaml_data import data
from Libraries.other_tools.setting import get_file_full_path,get_curr_path

COMMON_CONFIG = data.get_yaml_data(get_file_full_path("\\danta_common\\config.yaml"))

if __name__ == "__main__":
    # print('config', COMMON_CONFIG)
    # print(type(COMMON_CONFIG))
    print(get_file_full_path("\\danta_common\\config.yaml"))

