from locators import MainPageLocators
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains



class MainPage(BasePage):
    def __init__(self, driver, browser):
        super().__init__(driver)
        self.url = "https://stellarburgers.nomoreparties.site/"
        self.set_browser(browser)

    def open(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(MainPageLocators.LOGIN_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def click_login_button(self):
        try:
            if self._browser == "firefox":
                self.scroll_to_element(MainPageLocators.LOGIN_BUTTON)
                self.click_virt_mouse(MainPageLocators.LOGIN_BUTTON)
            else:
                self.click_element(MainPageLocators.LOGIN_BUTTON)
            return True
        except TimeoutException:
            return False

    def click_personal_account_button(self):
        try:
            if self._browser == "firefox":
                self.scroll_to_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
                self.click_virt_mouse(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
            else:
                self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
            return True
        except TimeoutException:
            return False

    def click_constructor_button(self):
        try:
            if self._browser == "firefox":
                self.scroll_to_element(MainPageLocators.CONSTRUCTOR_BUTTON)
                self.click_virt_mouse(MainPageLocators.CONSTRUCTOR_BUTTON)
            else:
                self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)
            return True
        except TimeoutException:
            return False

    def click_order_feed_button(self):
        try:
            if self._browser == "firefox":
                self.scroll_to_element(MainPageLocators.ORDER_FEED_BUTTON)
                self.click_virt_mouse(MainPageLocators.ORDER_FEED_BUTTON)
            else:
                self.click_element(MainPageLocators.ORDER_FEED_BUTTON)
            return True
        except TimeoutException:
            return False

    def click_ingredient(self, drag_and_drop=False):
        try:
            print(f"Клик по ингредиенту в {self._browser}, drag_and_drop={drag_and_drop}")
            if drag_and_drop and self._browser == "firefox":
                self.scroll_to_element(MainPageLocators.INGREDIENT)
                self.move_element(
                    MainPageLocators.INGREDIENT,
                    (By.CLASS_NAME, "BurgerConstructor_basket__list__l9dp_")
                )
            else:
                if self._browser == "firefox":
                    self.scroll_to_element(MainPageLocators.INGREDIENT)
                    self.click_virt_mouse(MainPageLocators.INGREDIENT)
                else:
                    self.click_element(MainPageLocators.INGREDIENT)
            visible = self.is_element_visible(MainPageLocators.INGREDIENT_DETAILS)
            print(f"Модальное окно с деталями видно: {visible}")
            return True
        except TimeoutException as e:
            print(f"Ошибка при клике по ингредиенту: {e}")
            return False

    def get_ingredient_counter(self):
        try:
            counter = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.INGREDIENT_COUNTER)
            )
            return counter.text or "0"
        except TimeoutException:
            return "0"

    def click_order_button(self):
        try:
            #counter = self.get_ingredient_counter()
            if self._browser == "firefox":
                self.scroll_to_element(MainPageLocators.ORDER_BUTTON)
                self.click_virt_mouse(MainPageLocators.ORDER_BUTTON)
            else:
                self.click_element(MainPageLocators.ORDER_BUTTON)
            return True
        except TimeoutException as e:
            self.driver.save_screenshot("click_order_button_error.png")
            return False

    def click_close_modal(self):
        try:
            if self._browser == "firefox":
                self.scroll_to_element(MainPageLocators.CLOSE_MODAL)
                self.click_virt_mouse(MainPageLocators.CLOSE_MODAL)
            else:
                self.click_element(MainPageLocators.CLOSE_MODAL)
            return True
        except TimeoutException:
            return False

    def get_order_number(self):
        try:
            order_number_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER_MODAL)
            )
            order_number = ''.join(filter(str.isdigit, order_number_element.text))
            return order_number
        except TimeoutException:
            return None

    def add_ingredients_to_order(self, count=5):
        try:
            print(f"Добавление ингредиентов в {self._browser}")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(MainPageLocators.INGREDIENT)
            )
            drop_target_locator = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket')]")
            if self._browser == "firefox":
                self.scroll_to_element(drop_target_locator)
                # Булка
                bun_locator = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']")
                self.scroll_to_element(bun_locator)
                self.move_element(bun_locator, drop_target_locator)
                self.move_element(bun_locator, drop_target_locator)
                # Соус
                sauce_locator = (By.XPATH, "//img[@alt='Соус Spicy-X']")
                self.scroll_to_element(sauce_locator)
                self.move_element(sauce_locator, drop_target_locator)
                # Начинки
                fillings = [
                    "//img[@alt='Мясо бессмертных моллюсков Protostomia']",
                    "//img[@alt='Филе Люминесцентного тетраодонтимформа']",
                    "//img[@alt='Хрустящие минеральные кольца']"
                ]
                for filling_xpath in fillings[:count-3]:
                    try:
                        filling_locator = (By.XPATH, filling_xpath)
                        self.scroll_to_element(filling_locator)
                        self.move_element(filling_locator, drop_target_locator)
                        print(f"Добавлен ингредиент: {filling_xpath}")
                    except Exception as e:
                        print(f"Ошибка при добавлении {filling_xpath}: {e}")
                        continue
            else:
                drop_target = self.find_element(drop_target_locator)
                bun = self.find_element((By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']"))
                ActionChains(self.driver).drag_and_drop(bun, drop_target).perform()
                ActionChains(self.driver).drag_and_drop(bun, drop_target).perform()
                sauce = self.find_element((By.XPATH, "//img[@alt='Соус Spicy-X']"))
                ActionChains(self.driver).drag_and_drop(sauce, drop_target).perform()
                fillings = [
                    "//img[@alt='Мясо бессмертных моллюсков Protostomia']",
                    "//img[@alt='Филе Люминесцентного тетраодонтимформа']",
                    "//img[@alt='Хрустящие минеральные кольца']"
                ]
                for filling_xpath in fillings[:count-3]:
                    try:
                        filling = self.find_element((By.XPATH, filling_xpath))
                        ActionChains(self.driver).drag_and_drop(filling, drop_target).perform()
                    except:
                        continue
            counter = self.get_ingredient_counter()
            print(f"Текущий счетчик ингредиентов: {counter}")
        except TimeoutException as e:
            print(f"Ошибка в add_ingredients_to_order: {e}")