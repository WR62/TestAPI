import pytest
from http import HTTPStatus


@pytest.mark.parametrize('add_url', ['posts/1', 'posts/50'])
def test_get_posts(client_jph, add_url):
    response = client_jph.get_response(add_url)
    assert response.status_code == HTTPStatus.OK


def test_get_all_posts(client_jph):
    response = client_jph.get_response('posts')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('data_', [{
    'title': 'Aaaaaaaaaaaa',
    'body': 'arm',
    'userId': 1
},
    {
        'title': 'Ohoooooooooo',
        'body': 'trunk',
        'userId': 1
    }
])
def test_create_post(client_jph, data_):
    response = client_jph.post_data(data=data_)
    assert response.status_code == HTTPStatus.CREATED


def test_update_post(client_jph):
    data_ = {
        'title': 'SevenNations',
        'body': 'Arbol',
        'userId': 1
    }
    response = client_jph.put_data(data=data_)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('add_url', ['posts?id=54', 'posts?userId=1'])
def test_filtering(client_jph, add_url):
    response = client_jph.get_response(add_url)
    assert response.status_code == HTTPStatus.OK
