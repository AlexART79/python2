from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from .base_page import BasePage
from .page_elements import *


class LoginPage(BasePage):
    login_form_username = (By.ID, "login-form-username")
    login_form_password = (By.ID, "login-form-password")
    login_form_login_btn = (By.ID, "login")

    login_form_error = (By.ID, "usernameerror")
    login_form_error_message = (By.CSS_SELECTOR, "#usernameerror p")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

        self.login_text = InputElement(self.driver, LoginPage.login_form_username)
        self.password_text = InputElement(self.driver, LoginPage.login_form_password)
        self.login_btn = InputElement(self.driver, LoginPage.login_form_login_btn)

    def login(self, username, password):
        self.login_text.value = username
        self.password_text.value = password

        self.login_btn.click()

    def is_login_success(self):
        try:
            w = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(LoginPage.login_form_error))

            return not w.is_displayed()
        except TimeoutException:
            return True

    def get_login_error_message(self):
        try:
            w = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(LoginPage.login_form_error_message))

            return w.text
        except TimeoutException:
            return ""
