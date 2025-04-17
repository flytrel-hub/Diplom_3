from locators import OrderFeedPageLocators
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class OrderFeedPage(BasePage):
    def __init__(self, driver, browser):
        super().__init__(driver)
        self.url = "https://stellarburgers.nomoreparties.site/feed"
        self.set_browser(browser)

    def open(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(OrderFeedPageLocators.ORDER_ITEM)
            )
            return True
        except TimeoutException:
            print("Ошибка при открытии ленты заказов")
            return False

    def click_first_order(self):
        try:
            print(f"Клик по ORDER_ITEM в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(OrderFeedPageLocators.ORDER_ITEM)
                self.click_virt_mouse(OrderFeedPageLocators.ORDER_ITEM)
            else:
                first_order = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(OrderFeedPageLocators.ORDER_ITEM)
                )
                first_order.click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_DETAILS)
            )
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по ORDER_ITEM: {e}")
            return False

    def click_order_feed_button(self):
        """Клик по кнопке перехода в ленту заказов"""
        try:
            print(f"Клик по ORDER_FEED_BUTTON в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(OrderFeedPageLocators.ORDER_FEED_BUTTON)
                self.click_virt_mouse(OrderFeedPageLocators.ORDER_FEED_BUTTON)
            else:
                self.click_element(OrderFeedPageLocators.ORDER_FEED_BUTTON)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по ORDER_FEED_BUTTON: {e}")
            return False

    def is_order_visible(self, order_number):
        """Проверка видимости заказа в ленте"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_ITEM)
            )
            orders = self.driver.find_elements(*OrderFeedPageLocators.ORDER_ITEM)
            for order in orders:
                if order_number in order.text:
                    return True
            return False
        except TimeoutException:
            return False

    def click_close_modal(self):
        """Закрытие модального окна с деталями заказа"""
        try:
            print(f"Клик по MODAL_CLOSE_BUTTON в {self._browser}")
            if self._browser == "firefox":
                self.scroll_to_element(OrderFeedPageLocators.MODAL_CLOSE_BUTTON)
                self.click_virt_mouse(OrderFeedPageLocators.MODAL_CLOSE_BUTTON)
            else:
                self.click_element(OrderFeedPageLocators.MODAL_CLOSE_BUTTON)
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по MODAL_CLOSE_BUTTON: {e}")
            return False

    def is_order_details_visible(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_DETAILS)
            )
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_NUMBER)
            )
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_NAME)
            )
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_STATUS)
            )
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_INGREDIENTS_LIST)
            )
            return True
        except TimeoutException:
            return False

    def get_order_status(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_STATUS)
            ).text
        except TimeoutException:
            return None

    def get_order_ingredients(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_INGREDIENTS_LIST)
            ).text
        except TimeoutException:
            return None

    def get_total_orders_count(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.TOTAL_ORDERS_COUNTER)
            ).text
        except TimeoutException:
            return "0"

    def get_today_orders_count(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.TODAY_ORDERS_COUNTER)
            ).text
        except TimeoutException:
            return "0"

    def get_in_progress_orders(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.IN_PROGRESS_ORDERS)
            ).text
        except TimeoutException:
            return ""

    def get_order_details(self, order_number):
        """Получение деталей заказа"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_DETAILS_MODAL)
            )
            order_details = {
                'number': self.driver.find_element(*OrderFeedPageLocators.ORDER_DETAILS_NUMBER).text,
                'name': self.driver.find_element(*OrderFeedPageLocators.ORDER_NAME).text,
                'ingredients': self.driver.find_elements(*OrderFeedPageLocators.ORDER_INGREDIENTS_LIST)
            }
            return order_details
        except TimeoutException:
            return None