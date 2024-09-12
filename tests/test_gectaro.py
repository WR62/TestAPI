import pytest
from _datetime import datetime
from model import ListRequestStructure, RequestStructure


COMP_ID = 7323
PROJECT_ID = 85877


def test_list_requests(client, url, token):
    response = client.get_project_request_list()
    list_of_requests = ListRequestStructure(full_list=response.json())
    assert response.status_code == 200
    assert len(list_of_requests.full_list) > 0

    # Negative tests
    client.project_id = 111
    response = client.get_project_request_list()
    assert response.status_code > 400

    client.project_id = PROJECT_ID
    client.base_url = "https://api.gectaro.com"
    response = client.get_project_request_list()
    assert response.status_code == 404

    client.base_url = url


def test_add_request(client, url, token, resource):
    data = {
        'project_tasks_resource_id': resource,
        'volume': 14,
        'cost': 13.13,
        'needed_at': int(datetime.now().timestamp()),
        'is_over_budget': 1
    }
    response = client.post_resources_request(data=data)
    assert response.status_code == 201

    # Positive test #2
    data = {
        'project_tasks_resource_id': resource,
        'volume': 1313,
        'cost': 23.13,
        'needed_at': int(datetime.now().timestamp()),
        'is_over_budget': 1
    }
    response = client.post_resources_request(data=data)
    assert response.status_code == 201

    # # Negative test #1   project_tasks_resource_id' - 0
    data = {
        'project_tasks_resource_id': 0,
        'volume': 14,
        'cost': 13.13,
        'needed_at': int(datetime.now().timestamp()),
        'is_over_budget': 1
    }
    response = client.post_resources_request(data=data)
    assert response.status_code == 422

    # Negative test #2  volume - отрицательный
    data = {
        'project_tasks_resource_id': resource,
        'volume': -5,
        'cost': 13.13,
        'needed_at': int(datetime.now().timestamp()),
        'is_over_budget': 1
    }
    response = client.post_resources_request(data=data)
    assert response.status_code == 422  # Тест не должен проходить с отрицательным количеством, но он проходит


def test_get_request_info(client):
    # Получаем список заявок
    response = client.get_project_request_list()
    list_of_requests = ListRequestStructure(full_list=response.json())
    if len(list_of_requests.full_list) > 0:
        tmp = list_of_requests.full_list[0].id_
        response = client.get_request_info(tmp)
        assert response.status_code == 200
        assert response.json()['created_at'] > 0


@pytest.mark.parametrize('req_id', [0, -10])
def test_get_request_info_negative(client, req_id):
    response = client.get_request_info(req_id)
    assert response.status_code == 404


def test_change_request(client):
    # Получаем список заявок
    response = client.get_project_request_list()
    list_of_requests = ListRequestStructure(full_list=response.json())
    if len(list_of_requests.full_list) > 0:
        id_res = list_of_requests.full_list[0].id_
        response = client.get_request_info(id_res)
        request_info = RequestStructure(**response.json())
        # Меняем цену
        request_info.cost += 400
        response = client.change_request_info(id_res, data=request_info.dict())
        assert response.status_code == 200

        # Test 2
        id_res = list_of_requests.full_list[-1].id_
        response = client.get_request_info(id_res)
        request_info = RequestStructure(**response.json())
        # Меняем количество
        request_info.volume += 1000
        response = client.change_request_info(id_res, data=request_info.dict())
        if response.status_code == 200:
            response = client.get_request_info(id_res)
            request_info = RequestStructure(**response.json())
            assert request_info.volume > 100

        # Negative test
        response = client.change_request_info(0, data=request_info.dict())
        assert response.status_code == 404

        # Negative test 2
        request_info.created_at = None
        response = client.change_request_info(id_res, data=request_info.dict())
        assert response.status_code == 500


def test_delete_request(client):
    # Получаем список заявок
    response = client.get_project_request_list()
    list_of_requests = ListRequestStructure(full_list=response.json())
    if len(list_of_requests.full_list) > 0:
        # По ТЗ разрешено удалять только заявки сверх бюджета
        id_res = 0
        for item in list_of_requests.full_list:
            if item.is_over_budget == 1:
                id_res = item.id_
                break
        if id_res == 0:
            raise Exception('Request not found')
        response = client.delete_request(id_res)
        assert response.status_code == 204
        id_res = 0
        for item in reversed(list_of_requests.full_list):
            if item.is_over_budget == 1:
                id_res = item.id_
                break
        if id_res == 0:
            raise Exception('Request not found')
        response = client.delete_request(id_res)
        assert response.status_code == 204


@pytest.mark.parametrize('id_req', [0, None])
def test_delete_request_negative(client, id_req):
    response = client.delete_request(id_req)
    assert response.status_code == 404


def test_company_requests(client):
    response = client.get_company_requests(COMP_ID)
    assert response.status_code == 200
    list_of_requests = ListRequestStructure(full_list=response.json())
    assert len(list_of_requests.full_list) > 0


@pytest.mark.parametrize('comp_id', [0, None])
def test_company_requests_negative(client, comp_id):
    response = client.get_company_requests(comp_id)
    assert response.status_code == 404
