import allure
import time
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
            assert order_feed_page.is_element_visible(OrderFeedPageLocators.ORDER_DETAILS_MODAL), "Модальное окно с деталями заказа не отображается"

        with allure.step("Закрытие модального окна"):
            close_button = order_feed_page.find_element(OrderFeedPageLocators.MODAL_CLOSE_BUTTON)
            order_feed_page.execute_js_click(close_button)

        with allure.step("Проверка, что модальное окно закрылось"):
            try:
                order_feed_page.wait_for_element_not_visible(OrderFeedPageLocators.VISIBLE_MODAL, timeout=5)
            except TimeoutException:
                allure.attach(
                    order_feed_page.get_screenshot_as_png(),
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
            main_page.wait_for_element_clickable(MainPageLocators.ORDER_BUTTON)

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                main_page.wait_for_element_visible(MainPageLocators.ORDER_NUMBER_MODAL, timeout=15)
                for _ in range(3):
                    order_number = main_page.get_order_number()
                    if order_number and order_number != "9999":
                        break
                    main_page.wait_for_order_number_change(order_number)

                assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"

            except TimeoutException:
                allure.attach(
                    main_page.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Получение номера заказа"):
            order_number = main_page.get_order_number()

        with allure.step("Закрытие модального окна"):
            close_button = main_page.wait_for_element_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            main_page.execute_js_click(close_button)

        with allure.step("Переход в личный кабинет"):
            main_page.click_personal_account_button()

        with allure.step("Переход в историю заказов"):
            personal_account_page.click_order_history_button()

        with allure.step("Ожидание отображения заказа в истории"):
            main_page.wait_for_element_visible(OrderFeedPageLocators.ORDER_ITEM)

        with allure.step("Проверка наличия заказа в истории"):
            orders = main_page.find_elements(OrderFeedPageLocators.ORDER_NUMBER_TEXT)
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
            main_page.wait_for_element_clickable(MainPageLocators.ORDER_BUTTON)

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                main_page.wait_for_element_visible(MainPageLocators.ORDER_NUMBER_MODAL, timeout=15)
                for _ in range(3):
                    order_number = main_page.get_order_number()
                    if order_number and order_number != "9999":
                        break
                    main_page.wait_for_order_number_change(order_number)

                assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"
            except TimeoutException:
                allure.attach(
                    main_page.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Закрытие модального окна"):
            close_button = main_page.wait_for_element_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            main_page.execute_js_click(close_button)

        with allure.step("Возврат в ленту заказов"):
            main_page.click_order_feed_button()

        with allure.step("Ожидание обновления счетчика"):
            def counter_updated():
                new_count = int(order_feed_page.get_total_orders_count())
                return new_count > initial_count

            main_page.wait_for_counter_update(counter_updated)

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
            main_page.wait_for_element_clickable(MainPageLocators.ORDER_BUTTON)

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                main_page.wait_for_element_visible(MainPageLocators.ORDER_NUMBER_MODAL, timeout=15)
                for _ in range(3):
                    order_number = main_page.get_order_number()
                    if order_number and order_number != "9999":
                        break
                    main_page.wait_for_order_number_change(order_number)

                assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"
            except TimeoutException:
                allure.attach(
                    main_page.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Закрытие модального окна"):
            close_button = main_page.wait_for_element_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            main_page.execute_js_click(close_button)

        with allure.step("Возврат в ленту заказов"):
            main_page.click_order_feed_button()

        with allure.step("Ожидание обновления счетчика"):
            def counter_updated():
                new_count = int(order_feed_page.get_today_orders_count())
                time.sleep(2)
                return new_count > initial_count

            try:
                main_page.wait_for_counter_update(counter_updated, timeout=20)
            except TimeoutException:
                allure.attach(
                    main_page.get_screenshot_as_png(),
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
            main_page.wait_for_element_clickable(MainPageLocators.ORDER_BUTTON)

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Ожидание появления модального окна с номером заказа"):
            try:
                main_page.wait_for_element_visible(MainPageLocators.ORDER_NUMBER_MODAL, timeout=15)
            except TimeoutException:
                allure.attach(
                    main_page.get_screenshot_as_png(),
                    name="order_modal_not_visible",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

        with allure.step("Проверка отображения сообщения об успешном заказе"):
            assert main_page.is_element_visible(MainPageLocators.ORDER_SUCCESS), "Сообщение об успешном заказе не отобразилось"

        with allure.step("Получение номера заказа"):
            order_number = None
            for _ in range(3):
                order_number = main_page.get_order_number()
                if order_number and order_number != "9999":
                    break
                main_page.wait_for_order_number_change(order_number)

            assert order_number and order_number != "9999", "Не удалось получить валидный номер заказа"

        with allure.step("Закрытие модального окна"):
            close_button = main_page.wait_for_element_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            main_page.execute_js_click(close_button)

        with allure.step("Переход в ленту заказов"):
            order_feed_page.open()

        with allure.step("Ожидание, что список текущих заказов не пуст"):
            main_page.wait_for_element_not_present(
                OrderFeedPageLocators.ALL_ORDERS_READY_MESSAGE,
                timeout=15
            )

        with allure.step("Обновление страницы"):
            main_page.refresh_page()

        with allure.step("Проверка наличия заказа в разделе 'В работе'"):
            max_attempts = 15
            attempt = 0
            found = False
            order_in_progress = None

            while attempt < max_attempts and not found:
                try:
                    main_page.wait_for_element_present(OrderFeedPageLocators.IN_PROGRESS_ORDERS)

                    in_progress_orders = order_feed_page.find_elements(OrderFeedPageLocators.IN_PROGRESS_ORDERS)
                    order_numbers = [order.text.lstrip('0') for order in in_progress_orders]

                    allure.step(f"Попытка {attempt + 1}: Найдены заказы в работе: {order_numbers}")

                    if order_number in order_numbers:
                        order_in_progress = order_number
                        found = True
                        break

                except Exception as e:
                    allure.step(f"Ошибка на попытке {attempt + 1}: {str(e)}")

                time.sleep(2)
                attempt += 1

            if not found:
                allure.attach(
                    main_page.get_screenshot_as_png(),
                    name="order_not_in_progress",
                    attachment_type=allure.attachment_type.PNG
                )
            assert found, f'Заказ не появился в разделе "В работе" после {max_attempts} попыток: ожидалось {order_number}, получено {order_in_progress}.'