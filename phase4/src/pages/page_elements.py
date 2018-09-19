from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Element(object):
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    def find(self, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.locator))

    @property
    def text(self):
        return self.find().text

    @property
    def is_displayed(self):
        try:
            e = self.find(1)
            return e.is_displayed()
        except TimeoutException:
            return False

    def click(self):
        self.find().click()

    def clear(self):
        self.find().clear()

    def find_element(self, locator):
        return self.find().find_element(*locator)

    def find_elements(self, locator):
        return self.find().find_elements(*locator)

    def find_all(self, locator):
        return self.find().find_elements(*locator)

    def get_attribute(self, name):
        return self.find().get_attribute(name)

    def get_property(self, name):
        return self.find().get_property(name)

    def send_keys(self, value):
        self.find().send_keys(value)

    def wait(self, cond, timeout=30):
        return WebDriverWait(self.driver, timeout).until(cond)

    def wait_to_be_displayed(self, timeout=30):
        return self.wait(EC.visibility_of_element_located(self.locator), timeout)

    def wait_to_be_hidden(self, timeout=30):
        return self.wait(EC.invisibility_of_element_located(self.locator), timeout)

    def wait_to_be_enabled(self, timeout=30):
        return self.wait(EC.element_to_be_clickable(self.locator), timeout)


class InputElement(Element):
    @property
    def value(self):
        return self.find().get_attribute("value")

    @value.setter
    def value(self, val):
        sleep(5)
        self.find().clear()
        self.find().send_keys(val)


class TinyMceEditor(Element):
    @property
    def value(self):
        self.driver.switch_to.frame(self.find())
        content = Element(self.driver, (By.ID, "tinymce"))

        self.driver.switch_to.default_content()

        return content.text

    @value.setter
    def value(self, value):
        self.driver.switch_to.frame(self.find())
        content = Element(self.driver, (By.ID, "tinymce"))

        content.send_keys(value)

        self.driver.switch_to.default_content()


class SingleSelectElement(Element):
    def __init__(self, driver, locator):
        Element.__init__(self, driver, locator)

        by, loc_str = locator
        input_locator = (by, loc_str+"/input")
        self.input_element = InputElement(self.driver, input_locator)

    @property
    def value(self):
        return "NOT_IMPLEMENTED_YET"

    @value.setter
    def value(self, val):
        e = self.input_element.wait_to_be_enabled()
        if e:
            e.click()
            e.clear()
            e.send_keys(val)
            e.send_keys(Keys.RETURN)


class IssueListItem:
    link_locator = (By.TAG_NAME, "a")
    span_issue_key_locator = (By.CSS_SELECTOR, "a span.issue-link-key")
    span_issue_summary_locator = (By.CSS_SELECTOR, "a span.issue-link-summary")

    def __init__(self, driver, base_element):
        self.driver = driver
        self.base_element = base_element

    def select(self):
        a = self.base_element.find_element(*IssueListItem.link_locator)
        a.click()


class IssueDetails(Element):
    summary_val_locator = (By.ID, "summary-val")
    issue_link_locator = (By.CLASS_NAME, "issue-link")
    edit_link_locator = (By.CSS_SELECTOR, "#issue-content #edit-issue")
    description_content_locator = (By.CLASS_NAME, "user-content-block")
    type_val_locator = (By.ID, "type-val")
    priority_val_locator = (By.ID, "priority-val")

    def __init__(self, driver, locator):
        Element.__init__(self, driver, locator)

        self.issue_link = Element(self.driver, IssueDetails.issue_link_locator)
        self.edit_link = Element(self.driver, IssueDetails.edit_link_locator)
        self.summary_val = Element(self.driver, IssueDetails.summary_val_locator)
        self.description_content = Element(self.driver, IssueDetails.description_content_locator)
        self.type_val = Element(self.driver, IssueDetails.type_val_locator)
        self.priority_val = Element(self.driver, IssueDetails.priority_val_locator)

    def open_edit(self):
        sleep(5)
        self.edit_link.click()

    @property
    def summary(self):
        return self.summary_val.text.strip()


class CreateEditIssueDialog(Element):
    project_select_locator = (By.XPATH, "//*[@id='project-single-select']")

    issue_type_select_locator = (By.XPATH, "//*[@id='issuetype-single-select']")
    summary_locator = (By.XPATH, "//*[@id='summary']")
    description_iframe_locator = (By.XPATH, "//*[@id='description-wiki-edit']//iframe")
    issue_priority_select_locator = (By.XPATH, "//*[@id='priority-single-select']")

    submit_locator = (By.CSS_SELECTOR, ".jira-dialog input[type='Submit']")

    create_issue_error_locator = (By.CLASS_NAME, "error")

    def __init__(self, driver, locator):
        Element.__init__(self, driver, locator)

        self.project_select = SingleSelectElement(self.driver, CreateEditIssueDialog.project_select_locator)
        self.type_select = SingleSelectElement(self.driver, CreateEditIssueDialog.issue_type_select_locator)
        self.summary_text = InputElement(self.driver, CreateEditIssueDialog.summary_locator)
        self.description_element = TinyMceEditor(self.driver, CreateEditIssueDialog.description_iframe_locator)
        self.issue_priority = SingleSelectElement(self.driver, CreateEditIssueDialog.issue_priority_select_locator)
        self.submit_btn = Element(self.driver, CreateEditIssueDialog.submit_locator)

        self.create_issue_error = Element(self.driver, CreateEditIssueDialog.create_issue_error_locator)

    @property
    def project(self):
        return self.project_select.value

    @project.setter
    def project(self, value):
        self.project_select.value = value

    @property
    def issue_type(self):
        return self.type_select.value

    @issue_type.setter
    def issue_type(self, value):
        self.type_select.value = value

    @property
    def summary(self):
        return self.summary_text.value

    @summary.setter
    def summary(self, value):
        self.summary_text.value = value

    @property
    def description(self):
        return self.description_element.value

    @description.setter
    def description(self, value):
        self.description_element.value = value

    @property
    def priority(self):
        return self.issue_priority.value

    @priority.setter
    def priority(self, value):
        self.issue_priority.value = value

    def submit(self):
        self.submit_btn.wait_to_be_enabled(10)
        self.submit_btn.click()

    @property
    def error_message_is_displayed(self):
        try:
            self.create_issue_error.wait_to_be_displayed(10)
            return self.create_issue_error.is_displayed
        except TimeoutException:
            return False
