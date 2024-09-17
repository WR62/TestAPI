import requests


class DogCEO:
    def __init__(self, base_url):
        self.url = base_url
        self.session = requests.session()

    def get_response(self, add_url):
        response = self.session.get(f'{self.url}{add_url}')
        return response

