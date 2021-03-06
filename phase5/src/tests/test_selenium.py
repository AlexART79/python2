import json

import allure
import pytest
from allure_commons.types import AttachmentType

from ..DriverManager import DriverManager
from ..pages.pages import GeneralPage, DashboardPage, IssuesSearchPage, LoginPage
from ..rest.jira import Jira, prep_issues, prep_issue


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
    @allure.step
    @allure.tag('UI')
    @allure.feature('User management')
    @allure.story('Login')
    @allure.title("Test login attempt with wrong credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.uitest
    @pytest.mark.parametrize("login_data", [("alex_art", "test"),
                                            ("alex_art", ""),
                                            ("", ""),
                                            ("Alexander_Artemov", "test")])
    def test_login_incorrect(self, login_data, driver):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")
        login_page.login(*login_data)

        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        assert "your username and password are incorrect" in login_page.login_error_message

    @allure.step
    @allure.tag('UI')
    @allure.feature('User management')
    @allure.story('Login')
    @allure.title("Test login attempt with correct username and password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.uitest
    def test_login_correct(self, driver):
        login_page = LoginPage(driver)
        login_page.go("http://jira.hillel.it:8080/")

        login_page.login("Alexander_Artemov", "Alexander_Artemov")

        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
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

    @allure.step
    @allure.tag('UI')
    @allure.feature('Issues management')
    @allure.story('Create issue')
    @allure.title("Test create issue attempts with wrong data (no summary, summary too long etc.)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.uitest
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

        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        assert dashboard_page.create_issue_dialog.error_message_is_displayed

    @allure.step
    @allure.tag('UI')
    @allure.feature('Issues management')
    @allure.story('Create issue')
    @allure.title("Test create issue with correct data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.uitest
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

        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        # assert dashboard_page.aui_message_is_displayed
        assert issue_key is not None

        # save issue ID/Key for further cleanup
        if issue_key:
            TestIssues.issues.append(issue_key)

    @allure.step
    @allure.tag('UI')
    @allure.feature('Issues management')
    @allure.story('Search')
    @allure.title("Test search issues with different search conditions")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.uitest
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

        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        assert len(sp.found_issues) == search_data["res"]

    @allure.step
    @allure.tag('UI')
    @allure.feature('Issues management')
    @allure.story('Edit issue')
    @allure.title("Test update existing issue (summary/description/priority etc.)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.uitest
    @pytest.mark.parametrize("issue_data",
                             [{"summary": "AlexART - issue_edited_from_ui 1",
                               "description": "Description was updated from UI"},
                              {"summary": "AlexART - issue_edited_from_ui 2",
                               "priority": "High"}])
    def test_update_issue(self, driver, prep_issue, issue_data):
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

        sp.update(**issue_data)

        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        assert issue_data["summary"] == sp.issue_details.summary
