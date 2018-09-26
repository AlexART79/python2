import allure
from behave import *
from src import transform_parameters
from src import LoginPage


@allure.step
@given(u"open login page in browser")
def open_login_page_in_browser(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.go("http://jira.hillel.it:8080/")


@allure.step
@when(u'user logging in using "{username}", "{password}"')
@transform_parameters
def user_logging_in_using(context, username, password):
    context.login_page.login(username, password)


@allure.step
@then(u"user should be successfully logged in")
def user_should_be_successfully_logged_in(context):
    assert context.login_page.is_logged_in


@allure.step
@then(u"user should get a login error message")
def user_should_get_a_login_error_message(context):
    assert "your username and password are incorrect" in context.login_page.login_error_message
