import allure
from locators import MainPageLocators, OrderFeedPageLocators


class TestMainFunctionality:
    @allure.title("Проверка перехода в раздел 'Конструктор'")
    @allure.description("Тест проверяет, что при клике на кнопку 'Конструктор' отображается раздел с ингредиентами.")
    def test_constructor_navigation(self, main_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Клик по кнопке 'Конструктор'"):
            main_page.click_constructor_button()

        with allure.step("Проверка отображения раздела 'Конструктор'"):
            assert main_page.is_element_visible(MainPageLocators.INGREDIENT), "Конструктор не отображается"

    @allure.title("Проверка перехода в 'Ленту заказов'")
    @allure.description("Тест проверяет, что при клике на кнопку 'Лента заказов' отображается страница с заказами.")
    def test_order_feed_navigation(self, main_page, order_feed_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Клик по кнопке 'Лента заказов'"):
            main_page.click_order_feed_button()

        with allure.step("Проверка отображения 'Ленты заказов'"):
            assert order_feed_page.is_element_visible(OrderFeedPageLocators.ORDER_ITEM), "Лента заказов не отображается"

    @allure.title("Проверка отображения деталей ингредиента")
    @allure.description("Тест проверяет, что при клике на ингредиент открывается модальное окно с его деталями.")
    def test_ingredient_details(self, main_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Клик по ингредиенту"):
            main_page.click_ingredient()

        with allure.step("Проверка отображения модального окна с деталями ингредиента"):
            assert main_page.is_element_visible(MainPageLocators.INGREDIENT_DETAILS), "Всплывающее окно с деталями не отображается"

    @allure.title("Проверка закрытия окна с деталями ингредиента")
    @allure.description("Тест проверяет, что модальное окно с деталями ингредиента закрывается при клике на кнопку закрытия.")
    def test_close_ingredient_details(self, main_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Клик по ингредиенту"):
            main_page.click_ingredient()

        with allure.step("Проверка отображения модального окна с деталями"):
            assert main_page.is_element_visible(MainPageLocators.INGREDIENT_DETAILS), "Всплывающее окно с деталями не отображается"

        with allure.step("Клик по кнопке закрытия модального окна"):
            assert main_page.click_close_modal(), "Не удалось закрыть всплывающее окно"

        with allure.step("Проверка, что модальное окно закрылось"):
            assert not main_page.is_element_visible(MainPageLocators.INGREDIENT_DETAILS), "Всплывающее окно с деталями отображается после закрытия"

    @allure.title("Проверка увеличения счетчика ингредиентов")
    @allure.description("Тест проверяет, что при добавлении ингредиентов счетчик увеличивается.")
    def test_ingredient_counter(self, main_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Получение начального значения счетчика"):
            initial_counter = main_page.get_ingredient_counter()

        with allure.step("Добавление трех ингредиентов в заказ"):
            main_page.add_ingredients_to_order(count=3)

        with allure.step("Получение нового значения счетчика"):
            new_counter = main_page.get_ingredient_counter()

        with allure.step("Проверка увеличения счетчика"):
            assert int(new_counter) > int(initial_counter), "Каунтер ингредиента не увеличился"

    @allure.title("Проверка оформления заказа авторизованным пользователем")
    @allure.description("Тест проверяет, что авторизованный пользователь может успешно оформить заказ.")
    def test_order_creation(self, main_page, login_user, create_test_user):
        with allure.step("Авторизация пользователя"):
            login_user()

        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Добавление трех ингредиентов в заказ"):
            main_page.add_ingredients_to_order(count=3)

        with allure.step("Клик по кнопке 'Оформить заказ'"):
            main_page.click_order_button()

        with allure.step("Проверка успешного оформления заказа"):
            assert main_page.is_element_visible(MainPageLocators.ORDER_SUCCESS), "Не удалось оформить заказ для залогиненного пользователя"