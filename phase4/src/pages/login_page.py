from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from .base_page import BasePage
from .page_elements import *


class LoginPage(BasePage):
    login_form_username = (By.XPATH, "//input[@id='login-form-username']")
    login_form_password = (By.XPATH, "//input[@id='login-form-password']")
    login_form_login_btn = (By.XPATH, "//*[@id='login']")
    login_form_error_message = (By.XPATH, "//div[@id='usernameerror']/p")

    details_user_fullname = (By.XPATH, "//a[@id='header-details-user-fullname']")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

        self.login_text = InputElement(self.driver, LoginPage.login_form_username)
        self.password_text = InputElement(self.driver, LoginPage.login_form_password)
        self.login_btn = InputElement(self.driver, LoginPage.login_form_login_btn)

    def login(self, username, password):
        self.login_text.value = username
        self.password_text.value = password

        self.login_btn.click()

    @property
    def is_logged_in(self):
        try:
            details_user_fullname = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LoginPage.details_user_fullname))

            return details_user_fullname.is_displayed()
        except TimeoutException:
            return False

    @property
    def login_error_message(self):
        try:
            w = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LoginPage.login_form_error_message))

            return w.text
        except TimeoutException:
            return ""
