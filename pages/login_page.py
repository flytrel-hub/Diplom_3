from locators import LoginPageLocators
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class LoginPage(BasePage):
    def __init__(self, driver, browser):
        super().__init__(driver)
        self.set_browser(browser)
        self.url = "https://stellarburgers.nomoreparties.site/login"

    def open(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(LoginPageLocators.EMAIL_INPUT)
            )
            return True
        except TimeoutException:
            return False

    def input_email(self, email):
        try:
            email_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LoginPageLocators.EMAIL_INPUT)
            )
            email_input.clear()
            email_input.send_keys(email)
            return True
        except TimeoutException:
            return False

    def input_password(self, password):
        try:
            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LoginPageLocators.PASSWORD_INPUT)
            )
            password_input.clear()
            password_input.send_keys(password)
            return True
        except TimeoutException:
            return False

    def click_login_button(self):
        try:
            print(f"Клик по LOGIN_BUTTON в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(LoginPageLocators.LOGIN_BUTTON)
                self.click_virt_mouse(LoginPageLocators.LOGIN_BUTTON)
            else:
                self.click_element(LoginPageLocators.LOGIN_BUTTON)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по LOGIN_BUTTON: {e}")
            return False

    def click_forgot_password_link(self):
        try:
            forgot_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LoginPageLocators.FORGOT_PASSWORD_LINK)
            )
            forgot_link.click()
            return True
        except TimeoutException:
            return False

    def login(self, email, password):
        try:
            if not self.input_email(email):
                return False
            if not self.input_password(password):
                return False
            if not self.click_login_button():
                return False
            return True
        except TimeoutException:
            return False 