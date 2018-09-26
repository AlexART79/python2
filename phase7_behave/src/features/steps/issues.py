import json
import allure

from behave import *

from .common import transform_parameters
from ...pages.pages import GeneralPage, DashboardPage, IssuesSearchPage
from ...rest.jira import Jira
from ...rest.support import IssueInfo


@allure.step
@when(u"user added new issue with the parameters")
def user_added_new_issue_with_the_parameters(context):
    row = context.table[0]

    # create issue
    context.dashboard_page = GeneralPage(context.driver)
    context.issue_key = context.dashboard_page.create_issue(row["project"],
                                                            row["summary"],
                                                            row["type"],
                                                            row["description"],
                                                            row["priority"])

@allure.step
@then(u"issue should be successfully created")
def issue_should_be_successfully_created(context):
    # assert dashboard_page.aui_message_is_displayed
    assert context.issue_key is not None

    # save issue ID/Key for further cleanup
    if context.issue_key:
        context.issues.append(context.issue_key)


@allure.step
@when(u"user opened Create Issue dialog")
def user_opened_create_issue_dialog(context):
    context.dashboard_page = GeneralPage(context.driver)
    context.dashboard_page.open_create_issue_dialog()


@allure.step
@when(u"user selected propject '{project}' from the list")
def user_selected_propject(context, project):
    context.dashboard_page.create_issue_dialog.project = project


@allure.step
@when(u"user selected issue type '{issue_type}' from the list")
def user_selected_issue_type(context, issue_type):
    context.dashboard_page.create_issue_dialog.issue_type = issue_type


@allure.step
@when(u"user set summary '{summary}'")
@transform_parameters
def user_set_summary(context, summary):
    context.dashboard_page.create_issue_dialog.summary = summary


@allure.step
@when(u"user set description '{description}'")
def user_set_description(context, description):
    context.dashboard_page.create_issue_dialog.description = description


@allure.step
@when(u"user selected priority '{priority}' from the list")
def user_selected_priority(context, priority):
    context.dashboard_page.create_issue_dialog.priority = priority


@allure.step
@when(u"user press Create button")
def user_press_create_button(context):
    context.dashboard_page.create_issue_dialog.submit()
    context.issue_key = context.dashboard_page.get_created_issue_key()


@allure.step
@then(u'user should see error message')
def user_should_see_error_message(context):
    assert context.dashboard_page.create_issue_dialog.error_message_is_displayed


@allure.step
@given(u'there are some issues in jira')
def there_are_some_issues_in_jira(context):
    context.keys = []
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
        context.keys.append(data["key"])


@allure.step
@given(u'user is on issues search page')
def user_is_on_issues_search_page(context):
    context.dashboard_page = DashboardPage(context.driver)
    context.dashboard_page.go_to_search_page()


@allure.step
@when(u"user input '{jql}' string into search field")
def user_input_jql(context, jql):
    context.search_page = IssuesSearchPage(context.driver)
    context.search_page.fill_search_field(jql)


@allure.step
@when(u"press Enter key")
def press_enter_key(context):
    context.search_page.press_enter()
    context.search_page.wait_for_loading()


@allure.step
@then(u"there should be {result} issues found")
def there_should_be_result_issues_found(context, result):
    assert len(context.search_page.found_issues) == int(result)
