import pytest
from ..jira import Jira
from .fixtures.issue_info import IssueInfo, prep_issue

# issue tests: create/update/delete
class TestIssue:
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