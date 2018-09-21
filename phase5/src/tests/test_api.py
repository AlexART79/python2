import json
import random

import allure
import pytest
import requests

from ..rest.jira import Jira, prep_issue
from ..rest.support import AuthInfo, IssueInfo


# login tests: valid login and pass/invalid login/invalid pass
class TestLogin:
    @allure.step
    @allure.tag('API')
    @allure.feature('User management backend')
    @allure.story('Login')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("login_data", [AuthInfo("test", "test", 403),
                                            AuthInfo("Alexander_Artemov", "test", 401),
                                            AuthInfo("Alexander_Artemov", "Alexander_Artemov", 200)])
    def test_login(self, login_data):
        jira = Jira()

        r = requests.post(jira.auth_endpoint,
                          json=login_data.get_json(),
                          headers={"Content-Type": "application/json"})

        assert r.status_code == login_data.exp_status


class TestIssue:

    @allure.step
    @allure.tag('API')
    @allure.feature('Issues management backend')
    @allure.story('Create issue')
    @allure.severity(allure.severity_level.NORMAL)
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

        # cleanup: remove created issue
        if r.status_code == 201:
            data = json.loads(r.content)
            jira.delete_issue(data["key"])

    @allure.step
    @allure.tag('API')
    @allure.feature('Issues management backend')
    @allure.story('Delete issue')
    @allure.severity(allure.severity_level.CRITICAL)
    # id of issue to delete is provided by 'prep_issue' fixture
    def test_delete_issue(self, prep_issue):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        # delete issues by ID
        r = jira.delete_issue(prep_issue)

        assert r.status_code == 204  # deleted

    @allure.step
    @allure.tag('API')
    @allure.feature('Issues management backend')
    @allure.story('Update issue')
    @allure.severity(allure.severity_level.CRITICAL)
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

        #cleanup
        jira.delete_issue(prep_issue)

    @allure.step
    @allure.tag('API')
    @allure.feature('Issues management backend')
    @allure.story('Search issues')
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_issues(self, prep_issue):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        query = 'project=AQAPython AND type=Bug AND summary~"AA_issue_to_update"'
        r = jira.search_issues_g(query)
        assert r.status_code == 200

        data = json.loads(r.content)

        # verify that we received more than 0 issues
        assert data["total"] > 0

        # verify received data
        for issue in data["issues"]:
            assert "AA_issue_to_update" in issue["fields"]["summary"]  # summary contains desired substring
            assert issue["fields"]["project"]["name"] == 'AQAPython'    # project is AQAPython
            assert issue["fields"]["issuetype"]["name"] == 'Bug'        # issue type is Bug

        jira.delete_issue(prep_issue)

    @allure.step
    @allure.tag('API')
    @allure.feature('Issues management backend')
    @allure.story('Search issues (no results)')
    @allure.severity(allure.severity_level.TRIVIAL)
    @pytest.mark.flaky(reruns=3)
    def test_search_no_results(self):
        jira = Jira()
        jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

        query = 'summary~"no_issues_should_be_found"'
        r = jira.search_issues_g(query)
        assert r.status_code == 200

        data = json.loads(r.content)
        assert data["total"] == 0

        #random failing test (for re-runs)
        assert random.choice([True, False])