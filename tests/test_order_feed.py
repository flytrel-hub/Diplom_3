import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from locators import OrderFeedPageLocators, MainPageLocators


class TestOrderFeed:
    @allure.title("Проверка открытия модального окна с деталями заказа")
    @allure.description("Тест проверяет, что при клике на заказ открывается модальное окно с деталями, и оно корректно закрывается.")
    def test_order_details_modal(self, main_page, login_page, order_feed_page, personal_account_page):
        with allure.step("Открытие страницы ленты заказов"):
            order_feed_page.open()

        with allure.step("Клик по первому заказу в ленте"):
            order_item = order_feed_page.find_element(OrderFeedPageLocators.ORDER_ITEM)
            order_item.click()

        with allure.step("Проверка отображения модального окна с деталями заказа"):
            modal = order_feed_page.find_element(OrderFeedPageLocators.ORDER_DETAILS_MODAL)
            assert modal.is_displayed(), "Модальное окно с деталями заказа не отображается"

        with allure.step("Закрытие модального окна"):
            close_button = order_feed_page.find_element(OrderFeedPageLocators.MODAL_CLOSE_BUTTON)
            order_feed_page.driver.execute_script("arguments[0].click();", close_button)

        with allure.step("Проверка, что модальное окно закрылось"):
            try:
                WebDriverWait(order_feed_page.driver, 5).until_not(
                    EC.presence_of_element_located(OrderFeedPageLocators.VISIBLE_MODAL),
                    message="Модальное окно не закрылось"
                )
            except TimeoutException:
                allure.attach(
                    order_feed_page.driver.get_screenshot_as_png(),
                    name="modal_not_closed",
                    attachment_type=allure.attachment_type.PNG
                )
                assert False, "Модальное окно не закрылось после 5 секунд ожидания"

    @allure.title("Проверка отображения заказа пользователя в ленте")
    @allure.description("Тест создает заказ, проверяет его в истории заказов и в ленте заказов.")
    def test_user_orders_in_feed(self, main_page, login_page, order_feed_page, personal_account_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Добавление трех ингредиентов в заказ"):
            main_page.add_ingredients_to_order(count=3)

        with allure.step("Ожидание кликабельности кнопки 'Оформить заказ'"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON),
                message="Кнопка 'Оформить заказ' не стала кликабельной"
            )

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                WebDriverWait(main_page.driver, 15).until(
                    EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER_MODAL),
                    message="Модальное окно с номером заказа не появилось"
                )
                for _ in range(3):
                    order_number = WebDriverWait(main_page.driver, 10).until(
                        lambda x: main_page.get_order_number(),
                        message="Не удалось получить номер заказа"
                    )
                    if order_number and order_number != "9999":
                        break
                    WebDriverWait(main_page.driver, 5).until(
                        lambda x: main_page.get_order_number() != order_number,
                        message="Номер заказа не изменился"
                    )

                assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"

            except TimeoutException:
                allure.attach(
                    main_page.driver.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Получение номера заказа"):
            order_number = WebDriverWait(main_page.driver, 10).until(
                lambda x: main_page.get_order_number(),
                message="Не удалось получить номер заказа"
            )

        with allure.step("Закрытие модального окна"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON),
                message="Кнопка закрытия модального окна не стала кликабельной"
            )
            main_page.driver.execute_script("arguments[0].click();", 
                main_page.driver.find_element(*MainPageLocators.MODAL_CLOSE_BUTTON))

        with allure.step("Переход в личный кабинет"):
            main_page.click_personal_account_button()

        with allure.step("Переход в историю заказов"):
            personal_account_page.click_order_history_button()

        with allure.step("Ожидание отображения заказа в истории"):
            WebDriverWait(main_page.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_ITEM),
                message="Заказы не отобразились в истории"
            )

        with allure.step("Проверка наличия заказа в истории"):
            orders = main_page.driver.find_elements(By.XPATH, "//p[@class='text text_type_digits-default']")
            order_numbers = [order.text for order in orders]
            formatted_order_number = f"#0{order_number}"
            assert formatted_order_number in order_numbers, f"Заказ {formatted_order_number} не найден в истории заказов"

        with allure.step("Переход в ленту заказов"):
            main_page.click_order_feed_button()

        with allure.step("Проверка видимости заказа в ленте"):
            assert order_feed_page.is_order_visible(formatted_order_number), f"Заказ {formatted_order_number} не найден в ленте заказов"

    @allure.title("Проверка увеличения счетчика 'Выполнено за все время'")
    @allure.description("Тест создает заказ и проверяет, что счетчик 'Выполнено за все время' увеличивается.")
    def test_total_orders_counter_update(self, main_page, login_page, order_feed_page, personal_account_page):
        with allure.step("Переход в ленту заказов"):
            main_page.click_order_feed_button()

        with allure.step("Получение начального значения счетчика"):
            initial_count = int(order_feed_page.get_total_orders_count())

        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Добавление трех ингредиентов в заказ"):
            main_page.add_ingredients_to_order(count=3)

        with allure.step("Ожидание кликабельности кнопки 'Оформить заказ'"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON),
                message="Кнопка 'Оформить заказ' не стала кликабельной"
            )

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                WebDriverWait(main_page.driver, 15).until(
                    EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER_MODAL),
                    message="Модальное окно с номером заказа не появилось"
                )
                for _ in range(3):
                    order_number = WebDriverWait(main_page.driver, 10).until(
                        lambda x: main_page.get_order_number(),
                        message="Не удалось получить номер заказа"
                    )
                    if order_number and order_number != "9999":
                        break
                    WebDriverWait(main_page.driver, 5).until(
                        lambda x: main_page.get_order_number() != order_number,
                        message="Номер заказа не изменился"
                    )

                assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"
            except TimeoutException:
                allure.attach(
                    main_page.driver.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Закрытие модального окна"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON),
                message="Кнопка закрытия модального окна не стала кликабельной"
            )
            main_page.driver.execute_script("arguments[0].click();", 
                main_page.driver.find_element(*MainPageLocators.MODAL_CLOSE_BUTTON))

        with allure.step("Возврат в ленту заказов"):
            main_page.click_order_feed_button()

        with allure.step("Ожидание обновления счетчика"):
            def counter_updated(driver):
                new_count = int(order_feed_page.get_total_orders_count())
                return new_count > initial_count

            WebDriverWait(main_page.driver, 10).until(
                counter_updated,
                message="Счетчик 'Выполнено за все время' не обновился"
            )

        with allure.step("Проверка увеличения счетчика"):
            new_count = int(order_feed_page.get_total_orders_count())
            assert new_count > initial_count, "Счетчик 'Выполнено за все время' не увеличился после создания заказа"

    @allure.title("Проверка увеличения счетчика 'Выполнено за сегодня'")
    @allure.description("Тест создает заказ и проверяет, что счетчик 'Выполнено за сегодня' увеличивается.")
    def test_today_orders_counter_update(self, main_page, login_page, order_feed_page, personal_account_page):
        with allure.step("Переход в ленту заказов"):
            main_page.click_order_feed_button()

        with allure.step("Получение начального значения счетчика"):
            initial_count = int(order_feed_page.get_today_orders_count())

        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Добавление трех ингредиентов в заказ"):
            main_page.add_ingredients_to_order(count=3)

        with allure.step("Ожидание кликабельности кнопки 'Оформить заказ'"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON),
                message="Кнопка 'Оформить заказ' не стала кликабельной"
            )

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                WebDriverWait(main_page.driver, 15).until(
                    EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER_MODAL),
                    message="Модальное окно с номером заказа не появилось"
                )
                for _ in range(3):
                    order_number = WebDriverWait(main_page.driver, 10).until(
                        lambda x: main_page.get_order_number(),
                        message="Не удалось получить номер заказа"
                    )
                    if order_number and order_number != "9999":
                        break
                    WebDriverWait(main_page.driver, 5).until(
                        lambda x: main_page.get_order_number() != order_number,
                        message="Номер заказа не изменился"
                    )

                assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"
            except TimeoutException:
                allure.attach(
                    main_page.driver.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Закрытие модального окна"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON),
                message="Кнопка закрытия модального окна не стала кликабельной"
            )
            main_page.driver.execute_script("arguments[0].click();", 
                main_page.driver.find_element(*MainPageLocators.MODAL_CLOSE_BUTTON))

        with allure.step("Возврат в ленту заказов"):
            main_page.click_order_feed_button()

        with allure.step("Ожидание обновления счетчика"):
            def counter_updated(driver):
                new_count = int(order_feed_page.get_today_orders_count())
                time.sleep(2)
                return new_count > initial_count

            try:
                WebDriverWait(main_page.driver, 20).until(
                    counter_updated,
                    message="Счетчик 'Выполнено за сегодня' не обновился"
                )
            except TimeoutException:
                allure.attach(
                    main_page.driver.get_screenshot_as_png(),
                    name="counter_not_updated",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Проверка увеличения счетчика"):
            new_count = int(order_feed_page.get_today_orders_count())
            assert new_count > initial_count, "Счетчик 'Выполнено за сегодня' не увеличился после создания заказа"

    @allure.title("Проверка появления заказа в разделе 'В работе'")
    @allure.description("Тест создает заказ и проверяет, что его номер появляется в разделе 'В работе'.")
    def test_order_in_progress(self, main_page, login_page, order_feed_page, personal_account_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Добавление трех ингредиентов в заказ"):
            main_page.add_ingredients_to_order(count=3)

        with allure.step("Ожидание кликабельности кнопки 'Оформить заказ'"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON),
                message="Кнопка 'Оформить заказ' не стала кликабельной"
            )

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                WebDriverWait(main_page.driver, 15).until(
                    EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER_MODAL),
                    message="Модальное окно с номером заказа не появилось"
                )
            except TimeoutException:
                allure.attach(
                    main_page.driver.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Проверка отображения сообщения об успешном заказе"):
            assert main_page.is_element_visible(MainPageLocators.ORDER_SUCCESS), "Сообщение об успешном заказе не отобразилось"

        with allure.step("Получение номера заказа"):
            order_number = None
            for _ in range(3):
                order_number = WebDriverWait(main_page.driver, 10).until(
                    lambda x: main_page.get_order_number(),
                    message="Не удалось получить номер заказа"
                )
                if order_number and order_number != "9999":
                    break
                WebDriverWait(main_page.driver, 5).until(
                    lambda x: main_page.get_order_number() != order_number,
                    message="Номер заказа не изменился"
                )

            assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"

        with allure.step("Закрытие модального окна"):
            WebDriverWait(main_page.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON),
                message="Кнопка закрытия модального окна не стала кликабельной"
            )
            main_page.driver.execute_script("arguments[0].click();", 
                main_page.driver.find_element(*MainPageLocators.MODAL_CLOSE_BUTTON))

        with allure.step("Переход в ленту заказов"):
            main_page.driver.get("https://stellarburgers.nomoreparties.site/feed")

        with allure.step("Ожидание, что список текущих заказов не пуст"):
            WebDriverWait(main_page.driver, 15).until_not(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Все текущие заказы готовы!']")),
                message="Список текущих заказов остался пустым"
            )

        with allure.step("Обновление страницы"):
            main_page.driver.refresh()

        with allure.step("Проверка наличия заказа в разделе 'В работе'"):
            max_attempts = 15
            attempt = 0
            found = False
            order_in_progress = None

            while attempt < max_attempts and not found:
                try:
                    WebDriverWait(main_page.driver, 10).until(
                        EC.visibility_of_element_located(OrderFeedPageLocators.IN_PROGRESS_ORDERS),
                        message="Секция 'В работе' не отобразилась"
                    )

                    in_progress_orders = order_feed_page.find_elements(OrderFeedPageLocators.IN_PROGRESS_ORDERS)
                    order_numbers = [order.text.lstrip('0') for order in in_progress_orders]

                    allure.step(f"Попытка {attempt + 1}: Найдены заказы в работе: {order_numbers}")

                    if order_number in order_numbers:
                        order_in_progress = order_number
                        found = True
                        break

                except Exception as e:
                    allure.step(f"Ошибка на попытке {attempt + 1}: {str(e)}")

                WebDriverWait(main_page.driver, 2).until(lambda x: True)
                attempt += 1

            if not found:
                allure.attach(
                    main_page.driver.get_screenshot_as_png(),
                    name="order_not_in_progress",
                    attachment_type=allure.attachment_type.PNG
                )
            assert found, f'Заказ не появился в разделе "В работе" после {max_attempts} попыток: ожидалось {order_number}, получено {order_in_progress}.'