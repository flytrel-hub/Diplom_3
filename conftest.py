import pytest
import requests
import os
import random
import string
import allure
from selenium import webdriver
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.personal_account_page import PersonalAccountPage
from pages.order_feed_page import OrderFeedPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPageLocators
from pages.login_page import LoginPageLocators
from pages.personal_account_page import PersonalAccountPageLocators



def pytest_addoption(parser):
    """Добавляем аргумент командной строки для выбора браузера"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Выберите браузер: chrome или firefox"
    )


@pytest.fixture
def driver(request):
    """Фикстура для создания драйвера Chrome или Firefox"""
    browser = request.config.getoption("--browser")
    
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")  # Только ошибки
        options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Убирает DevTools и USB ошибки

        service = webdriver.ChromeService(log_path='nul') 
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("devtools.console.stdout.content", False)  # отключение вывода в консоль
        options.log.level = "fatal"  # можно 'trace', 'debug', 'config', 'info', 'warn', 'error', 'fatal'

        # Отключение логов от самого GeckoDriver
        service = webdriver.FirefoxService(log_path=os.devnull)  # на Windows можно 'nul' 
        driver = webdriver.Firefox(service=service, options=options)
    
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver, request):
    browser = request.config.getoption("--browser")
    return MainPage(driver, browser)


@pytest.fixture
def login_page(driver, request):
    browser = request.config.getoption("--browser")
    return LoginPage(driver, browser)


@pytest.fixture
def forgot_password_page(driver, request):
    browser = request.config.getoption("--browser")
    return ForgotPasswordPage(driver, browser)


@pytest.fixture
def personal_account_page(driver, request):
    browser = request.config.getoption("--browser")
    return PersonalAccountPage(driver, browser)


@pytest.fixture
def order_feed_page(driver, request):
    browser = request.config.getoption("--browser")
    return OrderFeedPage(driver, browser)


@pytest.fixture
def create_test_user():
    """Создает тестового пользователя через API и удаляет его после тестов"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email = f"test_{random_string}@example.com"
    password = "password"
    name = "Test User"
    
    url = "https://stellarburgers.nomoreparties.site/api/auth/register"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "name": name
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 403:
        url = "https://stellarburgers.nomoreparties.site/api/auth/login"
        response = requests.post(url, headers=headers, json={
            "email": email,
            "password": password
        })
    
    assert response.status_code in [200, 403], f"Не удалось создать/получить тестового пользователя. Код ответа: {response.status_code}"
    
    tokens = response.json()
    
    user_data = {
        "email": email,
        "password": password,
        "name": name,
        "tokens": tokens
    }
    
    yield user_data
    
    url = "https://stellarburgers.nomoreparties.site/api/auth/user"
    headers = {
        "Authorization": tokens["accessToken"],
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    assert response.status_code in [202, 403], "Не удалось удалить тестового пользователя"


@pytest.fixture
def login_user(driver, login_page, create_test_user):
    def _login_user():
        login_page.open()
        
        tokens = create_test_user["tokens"]
        
        driver.execute_script(f"window.localStorage.setItem('accessToken', '{tokens['accessToken']}');")
        driver.execute_script(f"window.localStorage.setItem('refreshToken', '{tokens['refreshToken']}');")
        
        login_page.input_email(create_test_user["email"])
        login_page.input_password(create_test_user["password"])
        login_page.click_login_button()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        )
    
    return _login_user


@pytest.fixture
def login_and_go_to_profile(main_page, login_page, personal_account_page, create_test_user):
    """Фикстура для авторизации и перехода в личный кабинет"""
    with allure.step("Открытие главной страницы"):
        main_page.open()

    with allure.step("Ожидание кнопки 'Личный кабинет'"):
        WebDriverWait(main_page.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        )

    with allure.step("Переход в личный кабинет"):
        main_page.click_personal_account_button()

    with allure.step("Проверка отображения формы входа"):
        login_page.is_element_visible(LoginPageLocators.EMAIL_INPUT), "Не отображается форма входа"

    with allure.step("Ввод email тестового пользователя"):
        login_page.input_email(create_test_user["email"])

    with allure.step("Ввод пароля тестового пользователя"):
        login_page.input_password(create_test_user["password"])

    with allure.step("Клик по кнопке 'Войти'"):
        login_page.click_login_button()

    with allure.step("Ожидание кнопки 'Личный кабинет' после входа"):
        WebDriverWait(main_page.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        )

    with allure.step("Повторный переход в личный кабинет"):
        main_page.click_personal_account_button()

    with allure.step("Ожидание URL страницы профиля"):
        WebDriverWait(main_page.driver, 10).until(
            lambda x: "account/profile" in x.current_url
        )

    with allure.step("Проверка отображения раздела профиля"):
        assert personal_account_page.is_element_visible(PersonalAccountPageLocators.PROFILE_SECTION), "Не отображается раздел профиля"


@pytest.fixture(autouse=True)
def setup(driver, main_page, login_page, order_feed_page, personal_account_page, login_user, request):
    """Фикстура для автоматической авторизации и управления драйвером для определённых классов"""
    # Применяем create_test_user и driver только для нужных классов
    if request.cls and request.cls.__name__ in ["TestOrderFeed", "TestPersonalAccount"]:
        with allure.step("Авторизация пользователя"):
            login_user()

    yield

    with allure.step("Закрытие модального окна, если оно открыто"):
        try:
            if main_page.is_element_visible(MainPageLocators.MODAL_CLOSE_BUTTON):
                driver.execute_script("arguments[0].click();", 
                    driver.find_element(*MainPageLocators.MODAL_CLOSE_BUTTON))
        except Exception:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="modal_close_error",
                attachment_type=allure.attachment_type.PNG
            )
            pass