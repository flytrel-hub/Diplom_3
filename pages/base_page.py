import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains



class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self._browser = None

    def set_browser(self, browser):
        """Устанавливает текущий браузер"""
        self._browser = browser

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator, time=10):
        with allure.step(f"Клик по элементу с локатором {locator} (браузер: {self._browser})"):
            element = WebDriverWait(self.driver, time).until(
                EC.element_to_be_clickable(locator),
                message=f"Can't click element by locator {locator}"
            )
            element.click()

    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def move_element(self, locator_source, locator_target):
        """Перемещает элемент drag-and-drop через JS (только для Firefox)"""
        if self._browser == "firefox":
            source = self.find_element(locator_source)
            target = self.find_element(locator_target)
            js_script = """
                function simulateDragDrop(sourceElement, targetElement) {
                    var dragStartEvent = new Event('dragstart', { bubbles: true, cancelable: true });
                    var dragOverEvent = new Event('dragover', { bubbles: true, cancelable: true });
                    var dropEvent = new Event('drop', { bubbles: true, cancelable: true });
                    sourceElement.dispatchEvent(dragStartEvent);
                    targetElement.dispatchEvent(dragOverEvent);
                    targetElement.dispatchEvent(dropEvent);
                }
                simulateDragDrop(arguments[0], arguments[1]);
            """
            self.driver.execute_script(js_script, source, target)
        else:
            source = self.find_element(locator_source)
            target = self.find_element(locator_target)
            action = ActionChains(self.driver)
            action.drag_and_drop(source, target).pause(5).perform()

    def scroll_to_element(self, locator):
        """Прокручивает к элементу"""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_virt_mouse(self, locator):
        """Кликает элемент с обработкой модального окна (только для Firefox)"""
        if self._browser == "firefox":
            with allure.step("Проверка и закрытие мешающего модального окна"):
                for _ in range(3):
                    try:
                        # Ищем модальное окно, исключая окно с номером заказа
                        modal = self.driver.find_element(By.CSS_SELECTOR, "[class*='Modal_modal__']:not([class*='OrderDetails_orderDetails__'])")
                        try:
                            close_button = self.driver.find_element(By.CSS_SELECTOR, "[class*='Modal_modal__close__']")
                            self.driver.execute_script("arguments[0].click();", close_button)
                            allure.step("Модальное окно закрыто через кнопку")
                        except:
                            self.driver.find_element(By.TAG_NAME, "body").click()
                            allure.step("Модальное окно закрыто кликом по телу")
                        WebDriverWait(self.driver, 5).until_not(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='Modal_modal__']:not([class*='OrderDetails_orderDetails__'])")),
                            message="Модальное окно не закрылось"
                        )
                        break
                    except (TimeoutException, Exception):
                        allure.step("Модальное окно не найдено или не мешает")
                        break

        with allure.step(f"Клик по элементу с локатором {locator}"):
            try:
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(locator))
                element = self.driver.find_element(*locator)
                if self._browser == "firefox":
                    action = ActionChains(self.driver)
                    action.click(on_element=element).perform()
                    allure.step("Клик выполнен через ActionChains")
                else:
                    element.click()
                    allure.step("Клик выполнен напрямую")
            except Exception:
                element = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", element)
                allure.step("Клик выполнен через JS")