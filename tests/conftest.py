from datetime import datetime
import pytest
from HttpClientGect import HttpClient2Gectaro


PROJECT_ID = 85877


def pytest_addoption(parser):
    parser.addoption('--url', default='https://api.gectaro.com/v1')
    parser.addoption('--token')


@pytest.fixture(scope='session')
def url(request):
    return request.config.getoption('--url')


@pytest.fixture(scope='session')
def token(request):
    return request.config.getoption('--token')


@pytest.fixture(scope='session')
def client(url, token):
    client = HttpClient2Gectaro(base_url=url, token=token, project_id=PROJECT_ID)
    yield client


@pytest.fixture
def resource(client):
    data = {
        "name": "res_for_test",
        "needed_at": int(datetime.now().timestamp()),
        "project_id": PROJECT_ID,
        "type": 1,
        "volume": 13,
    }

    resource_id = client.post_resources(data=data).json()["id"]

    yield resource_id
