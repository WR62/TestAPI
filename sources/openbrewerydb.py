import requests


class OpenBreweryDB:
    def __init__(self, base_url):
        self.url = base_url
        self.session = requests.session()

    def get_response(self, add_url):
        response = self.session.get(f'{self.url}{add_url}')
        return response

    def searching(self, query_):
        return self.get_response(f'search?query={query_}&per_page=30')

    def search_by_type(self, query_):
        full_query = f'?by_type={query_}&per_page=30'
        return self.get_response(full_query)

    def search_by_ids(self, query_):
        full_query = f'?by_ids={query_}'
        return self.get_response(full_query)
