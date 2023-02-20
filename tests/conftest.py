import pytest


@pytest.fixture(scope="function")
def my_fixture(request):
    call = request._pyfuncitem._obj
    print(call.args)