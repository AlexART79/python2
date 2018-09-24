import allure

from allure_commons.types import AttachmentType
from behave import *

from src.DriverManager import DriverManager
from src.pages.pages import GeneralPage, DashboardPage, IssuesSearchPage, LoginPage


@fixture
def selenium_browser_chrome(context):
    context.browser = DriverManager.chrome_driver()
    yield context.browser
    context.browser.quit()


def before_scenario(context, scenario):
    use_fixture(selenium_browser_chrome, context)


@allure.step
@allure.tag('UI')
@given("open login page in browser")
def open_login_page_in_browser(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.go("http://jira.hillel.it:8080/")
    allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)


@allure.step
@allure.tag('UI')
@when('user logging in using "{username}", "{password}"')
def user_logging_in_using(context, username, password):
    context.login_page.login(username, password)
    allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)


@allure.step
@allure.tag('UI')
@then("user should be successfully logged in")
def user_should_be_successfully_logged_in(context):
    allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
    assert context.login_page.is_logged_in


@allure.step
@allure.tag('UI')
@then("user should get a login error message")
def user_should_get_a_login_error_message(context):
    allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
    assert "your username and password are incorrect" in context.login_page.login_error_message
