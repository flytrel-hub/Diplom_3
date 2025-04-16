import allure
from locators import PersonalAccountPageLocators, LoginPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestPersonalAccount:
    @allure.title("Проверка перехода в личный кабинет")
    @allure.description("Тест проверяет, что пользователь может войти в личный кабинет после авторизации.")
    def test_personal_account_navigation(self, login_and_go_to_profile):
        login_and_go_to_profile
        # Проверка уже выполнена в фикстуре login_and_go_to_profile
        pass

    @allure.title("Проверка перехода в историю заказов")
    @allure.description("Тест проверяет, что пользователь может перейти в раздел истории заказов из личного кабинета.")
    def test_order_history_navigation(self, main_page, personal_account_page, login_and_go_to_profile):
        login_and_go_to_profile

        with allure.step("Клик по кнопке 'История заказов'"):
            personal_account_page.click_order_history_button()

        with allure.step("Ожидание URL страницы истории заказов"):
            WebDriverWait(main_page.driver, 10).until(
                lambda x: "account/order-history" in x.current_url
            )

        with allure.step("Проверка отображения кнопки истории заказов"):
            assert personal_account_page.is_element_visible(PersonalAccountPageLocators.ORDER_HISTORY_BUTTON), "Не отображается кнопка истории заказов"

    @allure.title("Проверка выхода из аккаунта")
    @allure.description("Тест проверяет, что пользователь может выйти из аккаунта и вернуться на страницу входа.")
    def test_logout(self, main_page, login_page, personal_account_page, login_and_go_to_profile):
        login_and_go_to_profile

        with allure.step("Клик по кнопке 'Выход'"):
            personal_account_page.click_logout_button()

        with allure.step("Ожидание URL страницы входа"):
            WebDriverWait(main_page.driver, 10).until(
                lambda x: "/login" in x.current_url
            )

        with allure.step("Проверка отображения формы входа после выхода"):
            assert login_page.is_element_visible(LoginPageLocators.EMAIL_INPUT), "Не отображается форма входа после выхода"