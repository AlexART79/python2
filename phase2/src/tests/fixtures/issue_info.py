import pytest
import json

from src.jira import Jira


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

        #return {"fields": {"project": {"key": self.project},"summary": self.summary,"description": self.description,"issuetype": {"name": self.type}}}

        return dict_asd


@pytest.fixture
def prep_issue():
    i = IssueInfo("AQAPYTHON", "AA004 - issue_to_be_deleted", "this is a test issue for delete test ", "Bug")

    jira = Jira()
    jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

    r = jira.create_issue(i)
    data = json.loads(r.content)

    return data["key"]
