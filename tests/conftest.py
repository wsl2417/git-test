import os
from Libraries.read_data.get_yaml_data import data
from Libraries import COMMON_CONFIG
from config.setting import get_curr_path
import pytest


CURR_PATH = get_curr_path()
# data = GetYamlData()

def get_test_data(yaml_file_name) -> dict:
    try:
        # get_file_full_pat
        current_dir = os.path.dirname(os.path.abspath('data/Example'))#获取当前路径

        data_file_path = os.path.join(current_dir, "Example", yaml_file_name)
        yaml_data = data.get_yaml_data(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data
#
#
example_data = get_test_data("login_example.yaml")
# api_data = get_test_data("api_test_data.yml")
# scenario_data = get_test_data("scenario_test_data.yml")




if __name__=="__main__":
    # print("base_data",CURR_PATH)
    result = get_test_data("login_example.yaml")
    print('yaml_data', result)