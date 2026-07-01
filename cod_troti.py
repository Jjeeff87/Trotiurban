from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class UrbanScooterOrderPage:
    """Page Object do formulário 'Para quem é a scooter' (Fazer pedido)."""

    # ====================================
    # LOCALIZADORES - Campos do formulário
    # ====================================

    FIRST_NAME_FIELD = (By.XPATH, '//input[contains(@placeholder, "Nome") and not(contains(@placeholder, "Sobrenome"))]')
    LAST_NAME_FIELD = (By.XPATH, '//input[contains(@placeholder, "Sobrenome")]')
    ADDRESS_FIELD = (By.XPATH, '//input[contains(@placeholder, "Endereço")]')
    METRO_STATION_FIELD = (By.XPATH, '//input[contains(@placeholder, "Estação de metrô")]')
    PHONE_FIELD = (By.XPATH, '//input[contains(@placeholder, "Telefone")]')

    METRO_STATION_SUGGESTION = (By.XPATH, '//div[contains(@class, "suggest")]//div[1]')

    # ====================================
    # LOCALIZADORES - Cookies
    # ====================================

    COOKIE_ACCEPT_BUTTON = (By.XPATH, '//button[contains(., "ceitar")]')
    COOKIE_BANNER = (By.XPATH, '//*[contains(text(), "cookies")]')

    # ====================================
    # INICIALIZAÇÃO
    # ====================================

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ====================================
    # UTILITÁRIOS
    # ====================================

    def _find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def _type(self, locator, text):
        element = self._find(locator)
        element.clear()
        element.send_keys(text)

    def _get_value(self, locator):
        return self._find(locator).get_attribute('value')

    def _get_border_color(self, locator):
        return self._find(locator).value_of_css_property('border-color')

    def _blur(self, locator):
        self._find(locator).send_keys(Keys.TAB)

    # ====================================
    # COOKIES
    # ====================================

    def accept_cookies_if_present(self):
        try:
            self._find(self.COOKIE_ACCEPT_BUTTON).click()
        except Exception:
            pass

    def is_cookie_banner_visible(self):
        try:
            return self._find(self.COOKIE_BANNER).is_displayed()
        except Exception:
            return False

    # ====================================
    # NOME
    # ====================================

    def set_first_name(self, value):
        self._type(self.FIRST_NAME_FIELD, value)
        self._blur(self.FIRST_NAME_FIELD)

    def get_first_name_value(self):
        return self._get_value(self.FIRST_NAME_FIELD)

    def get_first_name_border_color(self):
        return self._get_border_color(self.FIRST_NAME_FIELD)

    # ====================================
    # ENDEREÇO
    # ====================================

    def set_address(self, value):
        self._type(self.ADDRESS_FIELD, value)
        self._blur(self.ADDRESS_FIELD)

    def get_address_value(self):
        return self._get_value(self.ADDRESS_FIELD)

    def get_address_border_color(self):
        return self._get_border_color(self.ADDRESS_FIELD)

    # ====================================
    # ESTAÇÃO DE METRÔ
    # ====================================

    def set_metro_station(self, search_text):
        self._type(self.METRO_STATION_FIELD, search_text)
        self._find(self.METRO_STATION_SUGGESTION).click()

    def type_metro_station_free_text(self, text):
        """Digita um texto livre no campo (sem selecionar sugestão) e tira o foco."""
        self._type(self.METRO_STATION_FIELD, text)
        self._blur(self.METRO_STATION_FIELD)

    def get_metro_station_value(self):
        return self._get_value(self.METRO_STATION_FIELD)

    # ====================================
    # TELEFONE
    # ====================================

    def set_phone(self, value):
        self._type(self.PHONE_FIELD, value)
        self._blur(self.PHONE_FIELD)

    def get_phone_value(self):
        return self._get_value(self.PHONE_FIELD)

    def get_phone_border_color(self):
        return self._get_border_color(self.PHONE_FIELD)
