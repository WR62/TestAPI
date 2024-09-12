import requests


class HttpClient2Gectaro:
    def __init__(self, base_url, token, project_id):
        self.session = requests.Session()
        self.session.headers['Authorization'] = f'Bearer {token}'
        self.base_url = base_url
        self.project_id = project_id

    def get_project_request_list(self):
        response = self.session.get(f'{self.base_url}/projects/{self.project_id}/resource-requests',
                                    headers=self.session.headers)
        return response

    def post_resources(self, data: dict):
        response = self.session.post(
            f"{self.base_url}/projects/{self.project_id}/resources", json=data, headers=self.session.headers
        )
        return response

    def post_resources_request(self, data: dict):
        response = self.session.post(
            f"{self.base_url}/projects/{self.project_id}/resource-requests", json=data, headers=self.session.headers
        )
        return response

    def get_request_info(self, req_id):
        response = self.session.get(
            f"{self.base_url}/projects/{self.project_id}/resource-requests/{req_id}", headers=self.session.headers
        )
        return response

    def change_request_info(self, res_id, data: dict):
        response = self.session.put(
            f"{self.base_url}/projects/{self.project_id}/resource-requests/{res_id}", json=data, headers=self.session.
            headers
        )
        return response

    def delete_request(self, res_id):
        response = self.session.delete(
            f"{self.base_url}/projects/{self.project_id}/resource-requests/{res_id}", headers=self.session.
            headers
        )
        return response

    def get_company_requests(self, comp_id):
        response = self.session.get(
            f"{self.base_url}/companies/{comp_id}/resource-requests", headers=self.session.headers
        )
        return response
