import allure
from allure_commons.types import AttachmentType
from behave import *

from src.DriverManager import DriverManager
from src.pages.pages import GeneralPage, DashboardPage, IssuesSearchPage, LoginPage


@allure.step
@allure.tag('UI')
@given("open login page in browser")
def open_login_page_in_browser(context):
    context.driver = DriverManager.chrome_driver()
    context.login_page = LoginPage(context.driver)
    context.login_page.go("http://jira.hillel.it:8080/")
    allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)


@allure.step
@allure.tag('UI')
@when("user logging in using '{username}', '{password}'")
def user_logging_in_using(context, username, password):
    context.login_page.login(username, password)
    allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)


@allure.step
@allure.tag('UI')
@then("user should be successfully logged in")
def user_should_be_successfully_logged_in(context):
    allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
    assert context.login_page.is_logged_in
