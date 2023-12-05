import pytest
from tests.conftest import example_data
@pytest.fixture(scope="function")
def testcase_data(request):
    testcase_name = request.function.__name__
    return example_data.get(testcase_name)