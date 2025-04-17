from selenium.webdriver.common.by import By

class AuthLocators:
    RECOVER_PASSWORD_BUTTON = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    RECOVER_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    PASSWORD_VISIBILITY_TOGGLE = (By.XPATH, "//div[contains(@class, 'input__icon-action')]")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    PASSWORD_WRAPPER = (By.XPATH, "//div[contains(@class, 'input_type_password') and .//label[text()='Пароль']]")
    LOGIN_LINK = (By.XPATH, "//a[text()='Войти']")

class ConstructorLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//p[contains(text(), 'Конструктор')]")
    ORDER_FEED_LINK = (By.XPATH, "//p[text()='Лента Заказов']")
    INGREDIENT_ITEM = (By.XPATH, "(//a[@href='/ingredient/61c0c5a71d1f82001bdaaa6d'])")
    CLOSE_MODAL = (By.XPATH, "//button[contains(@class, 'close')]")
    INGREDIENT_COUNTER = (By.XPATH, "//h2[text()='Детали ингредиента']/ancestor::div[contains(@class, 'Modal_modal__container')]//button")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")

class ProfileLocators:
    PROFILE_LINK = (By.XPATH, "//p[contains(text(), 'Личный Кабинет')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(text(), 'История заказов')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")

class FeedLocators:
    ORDER_ITEM = (By.XPATH, "//li[contains(@class, 'OrderHistory_listItem') and .//p[contains(text(), '#0213166')]]")
    TOTAL_COMPLETED = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    TODAY_COMPLETED = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    IN_PROGRESS_ORDER = (By.XPATH, "//li[@class='text text_type_main-small' and (starts-with(text(), 'Все текущие заказы') or string-length(text()) = 7)]")

class MainPageLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[@href='/account']")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    INGREDIENT = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']")
    INGREDIENT_COUNTER = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']/parent::a//p")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    INGREDIENT_DETAILS = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]")
    ORDER_SUCCESS = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//h2")
    CLOSE_MODAL = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    ORDER_NUMBER_MODAL = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")

class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[text()='Восстановить пароль']")

class ForgotPasswordPageLocators:
    EMAIL_INPUT = (By.NAME, "email")
    RESET_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon')]")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//a[text()='Войти']")
    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(@class, 'input__error')]")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Сохранить']")

class PersonalAccountPageLocators:
    ORDER_HISTORY_BUTTON = (By.XPATH, "//a[@href='/account/order-history']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    PROFILE_BUTTON = (By.XPATH, "//a[@href='/account/profile']")
    PROFILE_SECTION = (By.XPATH, "//ul[contains(@class, 'Account_list')]")

class OrderFeedPageLocators:
    ORDER_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_textBox')]")
    ORDER_DETAILS = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    ORDER_NUMBER = (By.XPATH, "//p[contains(@class, 'text_type_digits-default')]")
    ORDER_NAME = (By.XPATH, "//h2[contains(@class, 'text_type_main-medium')]")
    ORDER_STATUS = (By.XPATH, "//p[contains(@class, 'text_type_main-default') and @style='color: rgb(0, 204, 204);']")
    ORDER_INGREDIENTS_LIST = (By.XPATH, "//ul[contains(@class, 'Modal_list__2sHWc')]")
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p[contains(@class, 'text_type_digits-large')]")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p[contains(@class, 'text_type_digits-large')]")
    IN_PROGRESS_ORDERS = (By.XPATH, "//ul[@class='OrderFeed_orderListReady__1YFem OrderFeed_orderList__cBvyi']/li[@class='text text_type_digits-default mb-2']")
    ORDER_DETAILS_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened__3ISw4') and contains(@class, 'Modal_modal__P3_V5')]")
    VISIBLE_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened__3ISw4') and contains(@class, 'Modal_modal__P3_V5') and contains(@style, 'visibility: visible')]")
    ORDER_NUMBER_TEXT = (By.XPATH, "//p[@class='text text_type_digits-default']")
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[contains(@class, 'OrderFeed_totalValue')]")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[contains(@class, 'OrderFeed_todayValue')]")
    ALL_ORDERS_READY_MESSAGE = (By.XPATH, "//p[text()='Все текущие заказы готовы!']") 