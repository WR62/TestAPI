import pytest
import requests


@pytest.fixture
def url_r(request):
    return request.config.getoption('--url_r')


@pytest.fixture
def status_cod(request):
    return int(request.config.getoption('status_cod'))


def test_status_code(url_r, status_cod):
    response = requests.session().get(url_r)
    assert response.status_code == status_cod
