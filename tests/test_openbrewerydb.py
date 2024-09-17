from http import HTTPStatus

import pytest


def test_random_brewery(client_brw):
    response = client_brw.get_response('random')
    assert response.status_code == HTTPStatus.OK and len(response.text) > 0


@pytest.mark.parametrize('add_url', ['?per_page=20', '?per_page=50',  '?per_page=100'])
def test_list_breweries(client_brw, add_url):
    response = client_brw.get_response(add_url)
    assert response.status_code == HTTPStatus.OK and len(response.text) > 0


@pytest.mark.parametrize('query_string', ['miami', 'paris', 'hamburg'])
def test_search(client_brw, query_string):
    response = client_brw.searching(query_string)
    assert response.status_code == HTTPStatus.OK and len(response.text) > 0


@pytest.mark.parametrize('type_', ['micro', 'large', 'bar', 'closed'])
def test_search_by_type(client_brw, type_):
    response = client_brw.search_by_type(type_)
    assert response.status_code == HTTPStatus.OK and len(response.text) > 0


def test_search_by_ids(client_brw):
    response = client_brw.get_response('?per_page=3')
    assert response.status_code == HTTPStatus.OK and len(response.text) > 0
    breweries = response.json()
    # Получаем произвольный список id для запроса
    full_query = ','.join(item['id'] for item in breweries)
    response = client_brw.search_by_ids(full_query)
    assert response.status_code == HTTPStatus.OK and len(response.text) > 0


