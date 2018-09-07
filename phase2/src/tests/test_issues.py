import pytest
import json
from ..jira import Jira
from .fixtures.issue_info import IssueInfo, prep_issue


# issue tests: create/update/delete
class TestIssue:

    @classmethod
    def teardown_class(cls):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")
        jira.cleanup()

    @pytest.mark.parametrize("issue_data", [IssueInfo(project="AQAPYTHON", description="this is a test issue. 01", type="Bug", expected=400),
                                            IssueInfo("AQAPYTHON", "", "this is issue with empty summary. 02", "Bug", 400),
                                            IssueInfo("AQAPYTHON", "AA001 - test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue test issue 02", "this is an issue with looooong text in summary. 03", "Bug", 400),
                                            IssueInfo("AQAPYTHON", "AA001 - test issue 03", "this is valid issue! 04", "Bug", 201)])
    def test_create_issue(self, issue_data):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        # create issue
        r = jira.create_issue(issue_data)
        assert r.status_code == issue_data.expected

    # id of issue to delete is provided by 'prep_issue' fixture
    def test_delete_issue(self, prep_issue):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        # delete issues by ID
        r = jira.delete_issue(prep_issue)

        assert r.status_code == 204  # deleted

    # id of issue to update is provided by 'prep_issue' fixture
    def test_update_issue(self, prep_issue):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        r = jira.update_issue(prep_issue, data={
            "fields": {
                "summary": "issue UPDATED",
                "description": "Description of UPDATED issue"
            }})
        assert r.status_code == 204 # updated

    def test_search_issues(self, prep_issue):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        query = 'project=AQAPython AND type=Bug AND summary~"issue_to_be_deleted"'
        r = jira.search_issues_g(query)
        assert r.status_code == 200

        data = json.loads(r.content)

        # verify that we received more than 0 issues
        assert data["total"] > 0

        # verify received data
        for issue in data["issues"]:
            assert "issue_to_be_deleted" in issue["fields"]["summary"]  # summary contains desired substring
            assert issue["fields"]["project"]["name"] == 'AQAPython'    # project is AQAPython
            assert issue["fields"]["issuetype"]["name"] == 'Bug'        # issue type is Bug

    def test_search_no_results(self):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        query = 'summary~"no_issues_should_be_found"'
        r = jira.search_issues_g(query)
        assert r.status_code == 200

        data = json.loads(r.content)
        assert data["total"] == 0