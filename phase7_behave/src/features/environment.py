import json
import logging
import allure

from allure_commons.types import AttachmentType
from behave import use_fixture, fixture
from behave.model_core import Status

from src.DriverManager import DriverManager
from src.rest import jira
from src.rest.jira import Jira

logging.basicConfig(level=logging.DEBUG)


@fixture
def driver(context):
    context.driver = DriverManager.chrome_driver()
    yield context.driver
    context.driver.quit()


def before_feature(context, feature):
    j = Jira()
    j.authenticate("Alexander_Artemov", "Alexander_Artemov")

    r = j.search_issues_g("creator = currentUser()")
    data = json.loads(r.content)

    # delete previously created issues (if found)
    for issue in data["issues"]:
        j.delete_issue(issue["key"])


def before_scenario(context, scenario):
    context.driver = DriverManager.chrome_driver()
    context.issues = []
    context.keys = []


def after_scenario(context, scenario):
    context.driver.quit()
    context.driver = None

    jira = Jira()
    jira.authenticate("Alexander_Artemov", "Alexander_Artemov")

    if context.issues:
        while len(context.issues) > 0:
            issue = context.issues.pop()
            jira.delete_issue(issue)

    if context.keys:
        while len(context.keys) > 0:
            issue = context.keys.pop()
            jira.delete_issue(issue)


def after_step(context, step):
    if step.status == Status.failed:
        allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot of " + step.name, attachment_type=AttachmentType.PNG)
