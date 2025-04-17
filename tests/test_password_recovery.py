import allure
from locators import ForgotPasswordPageLocators
from selenium.common.exceptions import TimeoutException


class TestPasswordRecovery:
    @allure.title("Проверка перехода на страницу восстановления пароля")
    @allure.description("Тест проверяет, что пользователь может перейти на страницу восстановления пароля через интерфейс.")
    def test_password_recovery_flow(self, main_page, login_page, forgot_password_page):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Переход в личный кабинет"):
            main_page.click_personal_account_button()

        with allure.step("Клик по ссылке 'Восстановить пароль'"):
            login_page.click_forgot_password_link()

        with allure.step("Проверка URL страницы восстановления пароля"):
            assert "forgot-password" in main_page.get_current_url(), "URL не содержит 'forgot-password'"

    @allure.title("Проверка процесса восстановления пароля")
    @allure.description("Тест проверяет ввод email и переход на страницу сброса пароля после клика по кнопке 'Восстановить'.")
    def test_click_recovery(self, main_page, login_page, forgot_password_page, create_test_user):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Переход в личный кабинет"):
            main_page.click_personal_account_button()

        with allure.step("Клик по ссылке 'Восстановить пароль'"):
            login_page.click_forgot_password_link()

        with allure.step("Ввод email тестового пользователя"):
            forgot_password_page.input_email(create_test_user["email"])

        with allure.step("Клик по кнопке 'Восстановить'"):
            forgot_password_page.click_reset_button()

        with allure.step("Ожидание кликабельности кнопки 'Сохранить'"):
            forgot_password_page.wait_for_element_clickable(ForgotPasswordPageLocators.SAVE_BUTTON)

        with allure.step("Проверка URL страницы сброса пароля"):
            assert "reset-password" in main_page.get_current_url(), "URL не содержит 'reset-password'"

    @allure.title("Проверка видимости поля пароля")
    @allure.description("Тест проверяет, что при клике на кнопку показа пароля поле становится видимым (тип поля меняется на 'text').")
    def test_password_field_visibility(self, main_page, login_page, forgot_password_page, create_test_user):
        with allure.step("Открытие главной страницы"):
            main_page.open()

        with allure.step("Переход в личный кабинет"):
            main_page.click_personal_account_button()

        with allure.step("Клик по ссылке 'Восстановить пароль'"):
            login_page.click_forgot_password_link()

        with allure.step("Ввод email тестового пользователя"):
            forgot_password_page.input_email(create_test_user["email"])

        with allure.step("Клик по кнопке 'Восстановить'"):
            forgot_password_page.click_reset_button()

        with allure.step("Ожидание кликабельности кнопки 'Показать пароль'"):
            try:
                forgot_password_page.wait_for_element_clickable(ForgotPasswordPageLocators.SHOW_PASSWORD_BUTTON)
                with allure.step("Клик по кнопке 'Показать пароль'"):
                    forgot_password_page.click_show_password_button()

                with allure.step("Проверка, что поле пароля стало видимым"):
                    assert forgot_password_page.get_password_field_type() == "text", "Поле пароля не стало видимым"
            except TimeoutException:
                allure.attach(
                    main_page.driver.get_screenshot_as_png(),
                    name="show_password_button_timeout",
                    attachment_type=allure.attachment_type.PNG
                )
                assert False, "Кнопка показать пароль не стала активной"