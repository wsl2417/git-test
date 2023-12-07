from Libraries.read_data.get_yaml_data import data
from config.setting import get_file_full_path

COMMON_CONFIG = data.get_yaml_data(get_file_full_path("\\config\\config.yaml"))

if __name__=="__main__":
    print('config',COMMON_CONFIG)
    print(type(COMMON_CONFIG))