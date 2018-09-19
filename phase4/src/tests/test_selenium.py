import json

import pytest
from ..DriverManager import DriverManager
from ..pages.login_page import LoginPage
from ..pages.general_page import GeneralPage, DashboardPage, IssuesSearchPage
from ..rest.jira import Jira

from ..rest.issue_info import prep_issues, prep_issue


# cleanup before test (remove leftovers from previous runs, if exists)
def setup_module(module):
    j = Jira()
    j.authenticate("Alexander_Artemov", "Alexander_Artemov")

    r = j.search_issues_g("creator = currentUser()")
    data = json.loads(r.content)

    # delete previously created issues (if found)
    for issue in data["issues"]:
        j.delete_issue(issue["key"])


# driver setup and teardown
@pytest.fixture
def driver():
    d = DriverManager.chrome_driver()
    yield d
    d.quit()


# rest-client setup and teardown
@pytest.fixture
def jira_rest():
    j = Jira()
    j.authenticate("Alexander_Artemov", "Alexander_Artemov")
    yield j


class BaseTest:
    pass


class TestLogin(BaseTest):

    @pytest.mark.parametrize("login_data", [("alex_art", "test"),
                                            ("alex_art", ""),
                                            ("", ""),
                                            ("Alexander_Artemov", "test")])
    def test_login_incorrect(self, login_data, driver):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login(*login_data)

        assert "your username and password are incorrect" in login_page.login_error_message

    def test_login_correct(self, driver):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")

        login_page.login("Alexander_Artemov", "Alexander_Artemov")
        assert login_page.is_logged_in


class TestIssues(BaseTest):
    issues = []

    def teardown_method(self, method):
        if TestIssues.issues:
            jira = Jira()
            jira.authenticate("Alexander_Artemov", "Alexander_Artemov")
            while len(TestIssues.issues) > 0:
                issue = TestIssues.issues.pop()
                jira.delete_issue(issue)

    @pytest.mark.parametrize("issue_data", [{"project": "AQAPython (AQAPYTHON)", "summary": "", "type": "Bug"},
                                            {"project": "AQAPython (AQAPYTHON)", "summary": "AlexART - " + "".join([str(x) for x in range(255)]),
                                             "type": "Bug"}])
    def test_create_issue_negative(self, issue_data, driver):
        # login
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        # create issue
        dashboard_page = GeneralPage(driver)
        dashboard_page.create_issue(**issue_data)

        assert dashboard_page.create_issue_dialog.error_message_is_displayed

    @pytest.mark.parametrize("issue_data", [{"project": "AQAPython (AQAPYTHON)", "summary": "AlexART - Test Story", "type": "Story",
                                             "description": "this is a test Story"},
                                            {"project": "AQAPython (AQAPYTHON)", "summary": "AlexART - Test Bug", "type": "Bug",
                                             "description": "this is a test Bug", "priority": "Medium"}])
    def test_create_issue_positive(self, issue_data, driver, jira_rest):
        # login
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        # create issue
        dashboard_page = GeneralPage(driver)
        issue_key = dashboard_page.create_issue(**issue_data)

        # assert dashboard_page.aui_message_is_displayed
        assert issue_key is not None

        # save issue ID/Key for further cleanup
        if issue_key:
            TestIssues.issues.append(issue_key)

    @pytest.mark.parametrize("search_data", [{"jql": "summary~'AA_issue_to_find'", "res": 5},
                                             {"jql": "summary~'AA_issue_to_find' AND issuetype = Story", "res": 1},
                                             {"jql": "summary~'AA_issue_to_find' AND issuetype = Epic", "res": 0}])
    def test_search_issues(self, search_data, driver, prep_issues):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        dashboard_page = DashboardPage(driver)
        dashboard_page.go_to_search_page()

        sp = IssuesSearchPage(driver)

        sp.search(search_data["jql"])

        assert len(sp.found_issues) == search_data["res"]

    def test_update_issue(self, driver, prep_issue):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        dashboard_page = DashboardPage(driver)
        dashboard_page.go_to_search_page()

        sp = IssuesSearchPage(driver)

        sp.search("summary~'AA_issue_to_update' AND issuetype = Bug")
        assert len(sp.found_issues) == 1

        sp.found_issues[0].select()
        sp.wait_for_loading()

        sp.update(**{"summary": "AlexART - issue_edited_from_ui", "priority": "High"})

        assert "AlexART - issue_edited_from_ui" == sp.issue_details.summary
