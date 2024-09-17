import pytest
from _datetime import datetime
from model import ListRequestStructure, RequestStructure
from http import HTTPStatus

from tests.HttpClientGect import HttpClient2Gectaro

COMP_ID = 7323
PROJECT_ID = 85877


def test_list_requests_positive_1(client, url, token):
    response = client.get_project_request_list()
    assert response.status_code == HTTPStatus.OK


def test_list_requests_positive_2(client, url, token):
    response = client.get_project_request_list()
    list_of_requests = ListRequestStructure(full_list=response.json())
    assert len(list_of_requests.full_list) > 0


def test_list_requests_negative_1(url, token):
    client_1 = HttpClient2Gectaro(base_url=url, token=token, project_id=111)
    response = client_1.get_project_request_list()
    assert response.status_code > 400


def test_list_requests_negative_2(url, token):
    client_2 = HttpClient2Gectaro(base_url="https://api.gectaro.com", token=token, project_id=PROJECT_ID)
    response = client_2.get_project_request_list()
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('data_',
                         [{
                             'volume': 14,
                             'cost': 13.13,
                             'needed_at': int(datetime.now().timestamp()),
                             'is_over_budget': 1
                         },
                             {
                                 'volume': 1313,
                                 'cost': 23.13,
                                 'needed_at': int(datetime.now().timestamp()),
                                 'is_over_budget': 1
                             }
                         ])
def test_add_request_positive(client, resource, data_):
    data_['project_tasks_resource_id'] = resource
    response = client.post_resources_request(data=data_)
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize('data_',
                         [{
                             'volume': 14,
                             'cost': -13.13,
                             'needed_at': int(datetime.now().timestamp()),
                             'is_over_budget': 1
                         },
                             {
                                 'volume': -5,
                                 'cost': 23.13,
                                 'needed_at': int(datetime.now().timestamp()),
                                 'is_over_budget': 1
                             }
                         ])
def test_add_request_negative(client, resource, data_):
    # Тесты не должны проходить с отрицательными значениями цены и количества
    data_['project_tasks_resource_id'] = resource
    response = client.post_resources_request(data=data_)
    assert response.status_code == 422


def test_get_request_info(client):
    # Получаем список заявок
    response = client.get_project_request_list()
    list_of_requests = ListRequestStructure(full_list=response.json())
    assert len(list_of_requests.full_list) > 0
    tmp = list_of_requests.full_list[0].id_
    response = client.get_request_info(tmp)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['created_at'] > 0


@pytest.mark.parametrize('req_id', [0, -10])
def test_get_request_info_negative(client, req_id):
    response = client.get_request_info(req_id)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_change_request_1(client):
    list_of_requests = client.get_full_list_of_requests()
    assert len(list_of_requests.full_list) > 0  # Проверяем, что список заявок непустой
    id_res = list_of_requests.full_list[0].id_
    response = client.get_request_info(id_res)
    request_info = RequestStructure(**response.json())
    # Меняем цену
    request_info.cost += 400
    response = client.change_request_info(id_res, data=request_info.dict())
    assert response.status_code == HTTPStatus.OK


def test_change_request_2(client):
    list_of_requests = client.get_full_list_of_requests()
    assert len(list_of_requests.full_list) > 0  # Проверяем, что список заявок непустой
    id_res = list_of_requests.full_list[-1].id_
    response = client.get_request_info(id_res)
    request_info = RequestStructure(**response.json())
    # Меняем количество
    request_info.volume += 1000
    response = client.change_request_info(id_res, data=request_info.dict())
    assert response.status_code == HTTPStatus.OK
    response = client.get_request_info(id_res)
    request_info = RequestStructure(**response.json())
    assert request_info.volume > 100


def test_change_request_negative_1(client):
    list_of_requests = client.get_full_list_of_requests()
    assert len(list_of_requests.full_list) > 0  # Проверяем, что список заявок непустой
    id_res = list_of_requests.full_list[-1].id_
    response = client.get_request_info(id_res)
    request_info = RequestStructure(**response.json())
    response = client.change_request_info(0, data=request_info.dict())
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_change_request_negative_2(client):
    list_of_requests = client.get_full_list_of_requests()
    assert len(list_of_requests.full_list) > 0  # Проверяем, что список заявок непустой
    id_res = list_of_requests.full_list[-1].id_
    response = client.get_request_info(id_res)
    request_info = RequestStructure(**response.json())
    request_info.created_at = None
    response = client.change_request_info(id_res, data=request_info.dict())
    assert response.status_code == 500


def test_delete_request_1(client):
    # Получаем список заявок
    list_of_requests = client.get_full_list_of_requests()
    assert len(list_of_requests.full_list) > 0
    # # По ТЗ разрешено удалять только заявки сверх бюджета
    # # Находим идентификатор первой заявки по порядку
    id_res = client.get_id_first_request(list_of_requests.full_list)
    assert id_res != 0, 'Request not found'
    response = client.delete_request(id_res)
    assert response.status_code == 204


def test_delete_request_2(client):
    # Получаем список заявок
    list_of_requests = client.get_full_list_of_requests()
    assert len(list_of_requests.full_list) > 0
    # # По ТЗ разрешено удалять только заявки сверх бюджета
    # # Находим идентификатор последней доступной заявки
    id_res = client.get_id_first_request(reversed(list_of_requests.full_list))
    assert id_res != 0, 'Request not found'
    response = client.delete_request(id_res)
    assert response.status_code == 204


@pytest.mark.parametrize('id_req', [0, None])
def test_delete_request_negative(client, id_req):
    response = client.delete_request(id_req)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_company_requests_1(client):
    response = client.get_company_requests(COMP_ID)
    assert response.status_code == HTTPStatus.OK


def test_company_requests_2(client):
    response = client.get_company_requests(COMP_ID)
    list_of_requests = ListRequestStructure(full_list=response.json())
    assert len(list_of_requests.full_list) > 0


@pytest.mark.parametrize('comp_id', [0, None])
def test_company_requests_negative(client, comp_id):
    response = client.get_company_requests(comp_id)
    assert response.status_code == HTTPStatus.NOT_FOUND
