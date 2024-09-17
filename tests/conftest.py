from datetime import datetime
import pytest
from HttpClientGect import HttpClient2Gectaro
from sources.dogceo import DogCEO
from sources.openbrewerydb import OpenBreweryDB
from tests.Jsonplaceholder import Jsonplaceholder

PROJECT_ID = 85877


def pytest_addoption(parser):
    parser.addoption('--url', default='https://api.gectaro.com/v1')
    parser.addoption('--token')
    parser.addoption('--urlph', default='https://jsonplaceholder.typicode.com/')
    parser.addoption('--urlbr', default='https://api.openbrewerydb.org/v1/breweries/')
    parser.addoption('--urldg', default='https://dog.ceo/api/breeds/')
    parser.addoption('--url_r', default='https://ya.ru')
    parser.addoption('--status_cod', default=200)


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


@pytest.fixture(scope='session')
def url_ph(request):
    return request.config.getoption('--urlph')


@pytest.fixture(scope='session')
def client_jph(url_ph):
    client_jph = Jsonplaceholder(base_url=url_ph)

    yield client_jph


@pytest.fixture(scope='session')
def url_br(request):
    return request.config.getoption('--urlbr')


@pytest.fixture(scope='session')
def client_brw(url_br):
    client_brw = OpenBreweryDB(base_url=url_br)

    yield client_brw


@pytest.fixture(scope='session')
def url_dg(request):
    return request.config.getoption('--urldg')


@pytest.fixture(scope='session')
def client_dog(url_dg):
    client_dog = DogCEO(base_url=url_dg)

    yield client_dog

