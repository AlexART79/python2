from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.pages.base_page import BasePage
from src.pages.page_elements import Element, InputElement, IssueListItem, IssueDetails, \
    CreateEditIssueDialog


class GeneralPage(BasePage):
    create_issue_link = (By.ID, "create_link")
    issues_menu_link = (By.ID, "find_link")
    issues_menu_dropdown = (By.ID, "find_link-content")
    issues_menu_item_search = (By.LINK_TEXT, "Search for issues")
    create_issue_dialog_locator = (By.ID, "create-issue-dialog")

    aui_message_container_locator = (By.ID, "aui-flag-container")
    aui_message_issue_link_locator = (By.CSS_SELECTOR, "#aui-flag-container a")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

        self.create_issue_link = Element(self.driver, GeneralPage.create_issue_link)
        self.issues_link = Element(self.driver, GeneralPage.issues_menu_link)
        self.issues_dropdown_menu = Element(self.driver, GeneralPage.issues_menu_dropdown)
        self.issues_menu_item_search = Element(self.driver, GeneralPage.issues_menu_item_search)
        self.create_issue_dialog = CreateEditIssueDialog(self.driver, GeneralPage.create_issue_dialog_locator)
        self.aui_message_container = Element(self.driver, GeneralPage.aui_message_container_locator)

    def create_issue(self, summary, type="Bug", description="", priority="Low"):
        self.create_issue_link.click()
        self.create_issue_dialog.issue_type = type
        self.create_issue_dialog.summary = summary
        self.create_issue_dialog.description = description
        self.create_issue_dialog.priority = priority
        self.create_issue_dialog.submit()

        if self.aui_message_is_displayed:
            e = self.aui_message_container.find_element(GeneralPage.aui_message_issue_link_locator)
            return e.text[:e.text.index(' ')]

        return ""

    @property
    def aui_message_is_displayed(self):
        try:
            e = self.aui_message_container.wait_for_display(10)
            return e.is_displayed
        except TimeoutException:
            return False

    def go_to_search_page(self):
        self.issues_link.click()
        self.issues_dropdown_menu.wait_for_display(3)
        self.issues_menu_item_search.click()


class DashboardPage(GeneralPage):
    pass


class IssuesSearchPage(GeneralPage):
    advanced_search = (By.ID, "advanced-search")
    issue_list_locator = (By.CSS_SELECTOR, "ol.issue-list")
    issue_content_locator = (By.ID, "issue-content")
    edit_issue_dialog_locator = (By.ID, "edit-issue-dialog")

    def __init__(self, driver):
        GeneralPage.__init__(self, driver)

        self.search_field = InputElement(self.driver, IssuesSearchPage.advanced_search)
        self.issue_list = Element(self.driver, IssuesSearchPage.issue_list_locator)
        self.issue_details = IssueDetails(self.driver, IssuesSearchPage.issue_content_locator)
        self.edit_issue_dialog = CreateEditIssueDialog(self.driver, IssuesSearchPage.edit_issue_dialog_locator)

    def search(self, jql):
        self.search_field.value = jql
        self.search_field.send_keys(Keys.RETURN)

        # wait for display
        sleep(10)

    def update(self, summary=None, type=None, priority=None, description=None):
        self.issue_details.open_edit()
        sleep(10)

        if summary:
            self.edit_issue_dialog.summary = summary
        if type:
            self.edit_issue_dialog.issue_type = type
        if priority:
            self.edit_issue_dialog.priority = priority
        if description:
            self.edit_issue_dialog.description = description

        self.edit_issue_dialog.submit()

    @property
    def found_issues(self):
        l = []

        # if list is displayed, collect items and return the list
        if self.issue_list.is_displayed:
            # find all list items
            items = self.issue_list.find_elements((By.TAG_NAME, "li"))
            for item in items:
                l.append(IssueListItem(self.driver, item))

        return l