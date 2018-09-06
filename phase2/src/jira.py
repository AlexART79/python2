import requests
from .tests.fixtures.login_info import AuthInfo

# class for JIRA manipulations
class Jira:
    def __init__(self):
        self.__base_URL = "http://jira.hillel.it:8080/rest/"
        self.__auth_endpoint = "auth/1/session"
        self.__issue_endpoint = "api/2/issue"
        self.__session = requests.Session()

    #
    # properties
    #

    @property
    def auth_endpoint(self):
        return self.__base_URL + self.__auth_endpoint

    @property
    def issue_endpoint(self):
        return self.__base_URL + self.__issue_endpoint

    #
    # Methods
    #

    def authenticate(self, login, passw):
        login_data = AuthInfo(login, passw, 200)

        self.__session.headers = {"Content-Type": "application/json"}
        r = self.__session.post(self.auth_endpoint, json=login_data.get_json())
        return r

    def create_issue(self, issue):
        r = self.__session.post(self.issue_endpoint, json=issue.get_json())
        return r

    def update_issue(self, key_id, data):
        r = self.__session.put(self.issue_endpoint + "/" + key_id, json=data)
        return r

    def delete_issue(self, key_id):
        r = self.__session.delete(self.issue_endpoint + "/" + key_id)
        return r
