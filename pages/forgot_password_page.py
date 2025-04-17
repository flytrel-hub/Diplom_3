from locators import AuthLocators
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time


class ForgotPasswordPage(BasePage):
    def __init__(self, driver, browser):
        super().__init__(driver)
        self.url = "https://stellarburgers.nomoreparties.site/forgot-password"
        self.set_browser(browser)

    def open(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(AuthLocators.EMAIL_INPUT)
            )
            return True
        except TimeoutException:
            print("Ошибка при открытии страницы восстановления пароля")
            return False

    def input_email(self, email, clear=True):
        try:
            print(f"Ввод email в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(AuthLocators.EMAIL_INPUT)
                self.click_virt_mouse(AuthLocators.EMAIL_INPUT)
            email_input = self.driver.find_element(*AuthLocators.EMAIL_INPUT)
            if clear:
                email_input.clear()
            email_input.send_keys(email)
            return True
        except Exception as e:
            print(f"Ошибка при вводе email: {e}")
            return False

    def click_reset_button(self):
        try:
            print(f"Клик по RECOVER_BUTTON в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(AuthLocators.RECOVER_BUTTON)
                self.click_virt_mouse(AuthLocators.RECOVER_BUTTON)
            else:
                self.click_element(AuthLocators.RECOVER_BUTTON)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по RECOVER_BUTTON: {e}")
            return False

    def click_show_password_button(self):
        try:
            print(f"Клик по PASSWORD_VISIBILITY_TOGGLE в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(AuthLocators.PASSWORD_VISIBILITY_TOGGLE)
                self.click_virt_mouse(AuthLocators.PASSWORD_VISIBILITY_TOGGLE)
            else:
                self.click_element(AuthLocators.PASSWORD_VISIBILITY_TOGGLE)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по PASSWORD_VISIBILITY_TOGGLE: {e}")
            return False

    def is_password_field_active(self):
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(AuthLocators.PASSWORD_INPUT)
            )
            return password_field.is_displayed() and password_field.is_enabled()
        except TimeoutException:
            return False

    def click_login_button(self):
        try:
            print(f"Клик по LOGIN_LINK в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(AuthLocators.LOGIN_LINK)
                self.click_virt_mouse(AuthLocators.LOGIN_LINK)
            else:
                self.click_element(AuthLocators.LOGIN_LINK)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по LOGIN_LINK: {e}")
            return False

    def is_success_message_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(AuthLocators.PASSWORD_WRAPPER)
            ).is_displayed()
        except TimeoutException:
            return False

    def input_code(self, code, clear=True):
        try:
            print(f"Ввод кода в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(AuthLocators.PASSWORD_INPUT)
                self.click_virt_mouse(AuthLocators.PASSWORD_INPUT)
            code_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(AuthLocators.PASSWORD_INPUT)
            )
            if clear:
                code_input.clear()
            code_input.send_keys(code)
            return True
        except TimeoutException as e:
            print(f"Ошибка при вводе кода: {e}")
            return False

    def click_save_button(self):
        try:
            print(f"Клик по RECOVER_BUTTON в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(AuthLocators.RECOVER_BUTTON)
                self.click_virt_mouse(AuthLocators.RECOVER_BUTTON)
            else:
                self.click_element(AuthLocators.RECOVER_BUTTON)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по RECOVER_BUTTON: {e}")
            return False

    def input_password(self, password):
        try:
            print(f"Ввод пароля в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(AuthLocators.PASSWORD_INPUT)
                self.click_virt_mouse(AuthLocators.PASSWORD_INPUT)
            password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(AuthLocators.PASSWORD_INPUT)
            )
            password_field.clear()
            password_field.send_keys(password)
            return True
        except TimeoutException as e:
            print(f"Ошибка при вводе пароля: {e}")
            return False

    def get_password_field_type(self):
        try:
            time.sleep(0.5)
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(AuthLocators.PASSWORD_INPUT)
            )
            for _ in range(3):
                field_type = password_field.get_attribute("type")
                if field_type in ["password", "text"]:
                    return field_type
                time.sleep(0.5)
            return password_field.get_attribute("type")
        except TimeoutException:
            return None