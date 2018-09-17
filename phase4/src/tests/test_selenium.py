from time import sleep

import pytest
from src.DriverManager import DriverManager
from src.pages.login_page import LoginPage
from src.pages.general_page import GeneralPage, DashboardPage, IssuesSearchPage
from ..rest.jira import Jira
from ..rest.issue_info import prep_issues

@pytest.fixture
def driver():
    d = DriverManager.chrome_driver()
    yield d
    d.quit()

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

        assert login_page.is_title_contains("Hillel")

        login_page.login(*login_data)

        assert not login_page.is_login_success()
        assert "your username and password are incorrect" in login_page.get_login_error_message()

    def test_login_correct(self, driver):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")

        assert login_page.is_title_contains("Hillel")

        login_page.login("Alexander_Artemov", "Alexander_Artemov")
        assert login_page.is_login_success()


class TestIssues(BaseTest):
    issues = []

    @classmethod
    def teardown_class(cls):
        if cls.issues:
            jira = Jira()
            jira.authenticate("Alexander_Artemov", "Alexander_Artemov")
            for issue in cls.issues:
                r = jira.delete_issue(issue)
                assert r.status_code == 204

    @pytest.mark.parametrize("issue_data", [{"summary": "", "type": "Bug"},
                                            {"summary": "AlexART - " + "".join([str(x) for x in range(255)]),
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

    @pytest.mark.parametrize("issue_data", [{"summary": "AlexART - Test Story", "type": "Story",
                                             "description": "this is a test Story"},
                                            {"summary": "AlexART - Test Bug", "type": "Bug",
                                             "description": "this is a test Bug", "priority": "Medium"}])
    def test_create_issue_positive(self, issue_data, driver):
        # login
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        # create issue
        dashboard_page = GeneralPage(driver)
        issue_key = dashboard_page.create_issue(**issue_data)

        assert dashboard_page.aui_message_is_displayed

        # save issue ID/Key for further cleanup
        TestIssues.issues.append(issue_key)

    @pytest.mark.parametrize("search_data", [{"jql": "creator=currentUser()", "res": 5},
                                             {"jql": "creator=currentUser() AND issuetype = Story", "res": 1},
                                             {"jql": "creator = currentUser() AND issuetype = Epic", "res": 0}])
    def test_search_issues(self, search_data, driver, prep_issues):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        dashboard_page = DashboardPage(driver)
        dashboard_page.go_to_search_page()

        sp = IssuesSearchPage(driver)

        sp.search(search_data["jql"])

        assert len(sp.found_issues) == search_data["res"]

    def test_update_issue(self, driver, prep_issues):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        dashboard_page = DashboardPage(driver)
        dashboard_page.go_to_search_page()

        sp = IssuesSearchPage(driver)

        sp.search("creator=currentUser() AND issuetype = Bug")
        assert len(sp.found_issues) == 4

        sp.found_issues[2].select()

        sp.update(**{"summary": "AlexART - issue_edited_from_ui", "priority": "High"})
        sleep(10)
        assert "AlexART - issue_edited_from_ui" == sp.issue_details.summary


