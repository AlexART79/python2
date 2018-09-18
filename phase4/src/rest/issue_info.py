import pytest
import json

from .jira import Jira

# class to store issue data for tests
class IssueInfo:
    def __init__(self, project=None, summary=None, description=None, type=None, expected=None):
        self.project = {"key": project} if project is not None else False
        self.summary = summary
        self.description = description
        self.type = {"name": type} if type is not None else False

        self.expected = expected

    def get_json(self):
        dict_asd = {"fields": {}}
        if self.project:
            dict_asd["fields"]['project'] = self.project

        if self.summary:
            dict_asd["fields"]['summary'] = self.summary
        if self.description:
            dict_asd["fields"]['description'] = self.description
        if self.type:
            dict_asd["fields"]['issuetype'] = self.type

        return dict_asd


# fixture to create issue before tests (for delete, update tests)
@pytest.fixture
def prep_issues():
    keys = []
    issues = [
         IssueInfo("AQAPYTHON", "AlexART - issue_to_be_found 1", "this is a test issue for delete/update test", "Story"),
         IssueInfo("AQAPYTHON", "AlexART - issue_to_be_found 2", "this is a test issue for delete/update test", "Bug"),
         IssueInfo("AQAPYTHON", "AlexART - issue_to_be_found 3", "this is a test issue for delete/update test", "Bug"),
         IssueInfo("AQAPYTHON", "AlexART - issue_to_be_found 4", "this is a test issue for delete/update test", "Bug"),
         IssueInfo("AQAPYTHON", "AlexART - issue_to_be_found 5", "this is a test issue for delete/update test", "Bug")]

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
    key = None

    ii = IssueInfo("AQAPYTHON", "AlexART - issue_to_be_updated 1", "this is a test issue for delete/update test", "Bug")

    jira = Jira()
    jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

    r = jira.create_issue(ii)
    data = json.loads(r.content)
    key = data["key"]

    yield key

    if key:
        jira.delete_issue(key)
