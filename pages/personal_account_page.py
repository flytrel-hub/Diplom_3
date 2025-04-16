from pages.base_page import BasePage
from locators import PersonalAccountPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class PersonalAccountPage(BasePage):
    def __init__(self, driver, browser):
        super().__init__(driver)
        self.url = "https://stellarburgers.nomoreparties.site/account/profile"
        self.set_browser(browser)

    def open(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(PersonalAccountPageLocators.ORDER_HISTORY_BUTTON)
            )
            return True
        except TimeoutException:
            print("Ошибка при открытии личного кабинета")
            return False

    def click_order_history_button(self):
        try:
            print(f"Клик по ORDER_HISTORY_BUTTON в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(PersonalAccountPageLocators.ORDER_HISTORY_BUTTON)
                self.click_virt_mouse(PersonalAccountPageLocators.ORDER_HISTORY_BUTTON)
            else:
                self.click_element(PersonalAccountPageLocators.ORDER_HISTORY_BUTTON)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по ORDER_HISTORY_BUTTON: {e}")
            return False

    def click_logout_button(self):
        try:
            print(f"Клик по LOGOUT_BUTTON в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(PersonalAccountPageLocators.LOGOUT_BUTTON)
                self.click_virt_mouse(PersonalAccountPageLocators.LOGOUT_BUTTON)
            else:
                self.click_element(PersonalAccountPageLocators.LOGOUT_BUTTON)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по LOGOUT_BUTTON: {e}")
            return False