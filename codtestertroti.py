import pytest
from selenium import webdriver

import data
import helpers
from cod_troti import UrbanScooterOrderPage


class TestUrbanScooterOrder:
    """Testes automatizados do formulário 'Para quem é a scooter' (Tarefa 1 - Web).

    Vários testes abaixo documentam bugs conhecidos (ver Jira JSQ-1 a JSQ-11) e
    são marcados com @pytest.mark.xfail: eles descrevem o comportamento CORRETO
    esperado, então falham propositalmente enquanto o bug não for corrigido.
    Quando o bug for corrigido, o teste passa a dar "XPASS", sinalizando que o
    xfail pode ser removido.
    """

    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_SCOOTER_URL):
            print("Conectado ao servidor Urban Scooter")
        else:
            print("Não foi possível conectar ao Urban Scooter. Verifique se o servidor está ligado "
                  "e atualize URBAN_SCOOTER_URL em data.py")

    def setup_method(self):
        self.driver.get(data.URBAN_SCOOTER_URL)
        self.page = UrbanScooterOrderPage(self.driver)
        self.page.accept_cookies_if_present()

    # ---------- JSQ-1: Endereço vazio não é validado ----------
    @pytest.mark.xfail(reason="BUG JSQ-1: campo Endereço vazio não mostra erro")
    def test_address_empty_should_show_error(self):
        self.page.set_first_name(data.FIRST_NAME)
        # Endereço propositalmente deixado vazio, apenas tira o foco do campo
        self.page.set_address("")

        assert self.page.get_address_border_color() == data.INVALID_BORDER_COLOR

    # ---------- JSQ-7: Nome com acento é rejeitado ----------
    @pytest.mark.xfail(reason="BUG JSQ-7: nome com acento (ex: 'José') é rejeitado incorretamente")
    def test_name_with_accent_should_be_accepted(self):
        self.page.set_first_name(data.NAME_WITH_ACCENT)

        assert self.page.get_first_name_border_color() == data.VALID_BORDER_COLOR

    # ---------- JSQ-8: Endereço com 50 caracteres (limite máx. documentado) é rejeitado ----------
    @pytest.mark.xfail(reason="BUG JSQ-8: endereço com 50 caracteres (limite documentado) é rejeitado")
    def test_address_max_length_50_should_be_accepted(self):
        self.page.set_address(data.ADDRESS_MAX_LENGTH_50)

        assert self.page.get_address_border_color() == data.VALID_BORDER_COLOR

    # ---------- JSQ-3: Telefone com 10 caracteres (limite mín. documentado) é rejeitado ----------
    @pytest.mark.xfail(reason="BUG JSQ-3: telefone com 10 caracteres (mínimo documentado) é rejeitado")
    def test_phone_min_length_10_should_be_accepted(self):
        self.page.set_phone(data.PHONE_MIN_LENGTH_10)

        assert self.page.get_phone_border_color() == data.VALID_BORDER_COLOR

    # ---------- JSQ-4: Telefone com 13 caracteres é aceito (deveria ser rejeitado) ----------
    @pytest.mark.xfail(reason="BUG JSQ-4: telefone com 13 caracteres é aceito, deveria ser rejeitado (máx. 12)")
    def test_phone_above_max_length_should_be_rejected(self):
        self.page.set_phone(data.PHONE_ABOVE_MAX_13)

        assert self.page.get_phone_border_color() == data.INVALID_BORDER_COLOR

    # ---------- JSQ-11: Nome/Sobrenome não removem espaços nas pontas ----------
    @pytest.mark.xfail(reason="BUG JSQ-11: espaços nas pontas do nome não são removidos (sem trim)")
    def test_first_name_should_trim_spaces(self):
        self.page.set_first_name("  Maria  ")

        assert self.page.get_first_name_value() == "Maria"

    # ---------- JSQ-6: Banner de cookies não desaparece ----------
    @pytest.mark.xfail(reason="BUG JSQ-6: banner de cookies continua visível mesmo após aceitar")
    def test_cookie_banner_should_disappear_after_accept(self):
        self.page.accept_cookies_if_present()

        assert not self.page.is_cookie_banner_visible()

    # ---------- Caso de sucesso (sem bug): dados válidos são aceitos ----------
    def test_valid_data_is_accepted(self):
        self.page.set_first_name(data.FIRST_NAME)
        self.page.set_address(data.ADDRESS)
        self.page.set_phone(data.PHONE_NUMBER)
        self.page.set_metro_station(data.METRO_STATION_SEARCH)

        assert self.page.get_first_name_border_color() == data.VALID_BORDER_COLOR
        assert self.page.get_address_border_color() == data.VALID_BORDER_COLOR
        assert self.page.get_phone_border_color() == data.VALID_BORDER_COLOR
        assert self.page.get_metro_station_value() == data.METRO_STATION_EXPECTED

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
