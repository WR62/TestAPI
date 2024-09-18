import requests


class Jsonplaceholder:
    def __init__(self, base_url):
        self.url = base_url
        self.session = requests.session()

    def get_response(self, add_url):
        response = self.session.get(f'{self.url}{add_url}')
        return response

    def post_data(self, data: dict):
        self.session.headers['Content-type'] = 'application/json; charset=UTF-8'
        response = self.session.post(
            f"{self.url}/posts", json=data, headers=self.session.headers
        )
        return response

    def put_data(self, data: dict):
        self.session.headers['Content-type'] = 'application/json; charset=UTF-8'
        response = self.session.put(
            f"{self.url}/posts/1", json=data, headers=self.session.headers
        )
        return response
