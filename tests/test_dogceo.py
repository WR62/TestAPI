import pytest

from http import HTTPStatus

from sources.dogceo import DogCEO


def test_list_all_breeds(client_dog):
    response = client_dog.get_response('list/all')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('amount_of_images', ['image/random/1', 'image/random/25', 'image/random/50'])
def test_random_image(client_dog, amount_of_images):
    response = client_dog.get_response(amount_of_images)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('breed', ['corgi', 'doberman', 'greyhound'])
def test_images_by_breed(breed):
    client_tmp = DogCEO(base_url='https://dog.ceo/api/breed/')
    response = client_tmp.get_response(add_url=f'{breed}/images')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('breed', ['boxer', 'dalmatian', 'labrador'])
def test_random_image_by_breed(breed):
    client_tmp = DogCEO(base_url='https://dog.ceo/api/breed/')
    response = client_tmp.get_response(add_url=f'{breed}/images/random')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('breed', ['terrier', 'spaniel', 'poodle'])
def test_all_sub_breeds_from_breed(breed):
    client_tmp = DogCEO(base_url='https://dog.ceo/api/breed/')
    response = client_tmp.get_response(add_url=f'{breed}/list')
    assert response.status_code == HTTPStatus.OK


def test_random_image_from_sub_breeds(breed='spaniel'):
    # Получить список sub-breeds
    client_tmp = DogCEO(base_url='https://dog.ceo/api/breed/')
    response = client_tmp.get_response(add_url=f'{breed}/list')
    assert response.status_code == HTTPStatus.OK
    list_of_sub_breeds = response.json()['message']
    for item in list_of_sub_breeds:
        response = client_tmp.get_response(add_url=f'{breed}/{item}/images/random')
        assert response.status_code == HTTPStatus.OK
