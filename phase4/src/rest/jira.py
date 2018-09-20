import pytest
import requests
import json
from .support import AuthInfo, IssueInfo


# class for JIRA manipulations
class Jira:

    __issues = []

    def __init__(self):
        self.__base_URL = "http://jira.hillel.it:8080/rest/"
        self.__auth_endpoint = "auth/1/session"
        self.__issue_endpoint = "api/2/issue"
        self.__search_endpoint = "api/2/search"

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

    @property
    def search_endpoint(self):
        return self.__base_URL + self.__search_endpoint

    #
    # Methods
    #

    def authenticate(self, login, passw):
        login_data = AuthInfo(login, passw)

        self.__session.headers = {"Content-Type": "application/json"}
        r = self.__session.post(self.auth_endpoint, json=login_data.get_json())

        return r

    def create_issue(self, issue):
        r = self.__session.post(self.issue_endpoint, json=issue.get_json())

        # if issue was created successfully, remember it's key for further cleanup
        if r.status_code == 201:
            data = json.loads(r.content)
            Jira.__issues.append(data["key"])

        return r

    def update_issue(self, key_id, data):
        r = self.__session.put(self.issue_endpoint + "/" + key_id, json=data)
        return r

    def delete_issue(self, key_id):
        r = self.__session.delete(self.issue_endpoint + "/" + key_id)
        return r

    def search_issues_p(self, jql):
        r = self.__session.post(self.search_endpoint, data=jql)
        return r

    def search_issues_g(self, jql):
        query = '?jql=' + jql
        r = self.__session.get(self.search_endpoint + query)
        return r

    def cleanup(self):
        for key in Jira.__issues:
            self.delete_issue(key)


# fixture to create issue before tests (for delete, update tests)
@pytest.fixture
def prep_issues():
    keys = []
    issues = [
         IssueInfo("AQAPYTHON", "AA_issue_to_find 1", "this is a test issue for delete/update test", "Story"),
         IssueInfo("AQAPYTHON", "AA_issue_to_find 2", "this is a test issue for delete/update test", "Bug"),
         IssueInfo("AQAPYTHON", "AA_issue_to_find 3", "this is a test issue for delete/update test", "Bug"),
         IssueInfo("AQAPYTHON", "AA_issue_to_find 4", "this is a test issue for delete/update test", "Bug"),
         IssueInfo("AQAPYTHON", "AA_issue_to_find 5", "this is a test issue for delete/update test", "Bug")]

    jira = Jira()
    jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

    for i in issues:
        r = jira.create_issue(i)
        data = json.loads(r.content)
        keys.append(data["key"])

    yield

    for k in keys:
        jira.delete_issue(k)

@pytest.fixture
def prep_issue():
    ii = IssueInfo("AQAPYTHON", "AA_issue_to_update 1", "this is a test issue for delete/update test", "Bug")

    jira = Jira()
    jira.authenticate("Alexander_Artemov", "Alexander_Artemov")
    r = jira.create_issue(ii)

    data = json.loads(r.content)
    key = data["key"] if data["key"] else None

    yield key

    if key:
        jira.delete_issue(key)
