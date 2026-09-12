import pytest
from selenium import webdriver

import data
import helpers
from cod_troti import UrbanScooterOrderPage


class TestUrbanScooterOrder:
    """Automated tests for the 'Who is the scooter for' form (Task 1 - Web).

    Several tests below document known bugs (see Jira JSQ-1 to JSQ-11) and
    are marked with @pytest.mark.xfail: they describe the CORRECT expected
    behavior, so they fail on purpose while the bug remains unfixed. Once
    the bug is fixed, the test starts giving "XPASS", signaling that the
    xfail can be removed.
    """

    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_SCOOTER_URL):
            print("Connected to the Urban Scooter server")
        else:
            print(
                "Could not connect to Urban Scooter. Check whether the server is up "
                "and update URBAN_SCOOTER_URL in data.py"
            )

    def setup_method(self):
        self.driver.get(data.URBAN_SCOOTER_URL)
        self.page = UrbanScooterOrderPage(self.driver)
        self.page.accept_cookies_if_present()

    # ---------- JSQ-1: Empty address is not validated ----------
    @pytest.mark.xfail(reason="BUG JSQ-1: empty Address field shows no error")
    def test_address_empty_should_show_error(self):
        self.page.set_first_name(data.FIRST_NAME)
        # Address left empty on purpose, just blurs the field
        self.page.set_address("")

        assert self.page.get_address_border_color() == data.INVALID_BORDER_COLOR

    # ---------- JSQ-7: Name with accent is rejected ----------
    @pytest.mark.xfail(reason="BUG JSQ-7: name with accent (e.g. 'José') is incorrectly rejected")
    def test_name_with_accent_should_be_accepted(self):
        self.page.set_first_name(data.NAME_WITH_ACCENT)

        assert self.page.get_first_name_border_color() == data.VALID_BORDER_COLOR

    # ---------- JSQ-8: Address with 50 chars (documented max limit) is rejected ----------
    @pytest.mark.xfail(
        reason="BUG JSQ-8: address with 50 characters (documented limit) is rejected"
    )
    def test_address_max_length_50_should_be_accepted(self):
        self.page.set_address(data.ADDRESS_MAX_LENGTH_50)

        assert self.page.get_address_border_color() == data.VALID_BORDER_COLOR

    # ---------- JSQ-3: Phone with 10 chars (documented min limit) is rejected ----------
    @pytest.mark.xfail(
        reason="BUG JSQ-3: phone with 10 characters (documented minimum) is rejected"
    )
    def test_phone_min_length_10_should_be_accepted(self):
        self.page.set_phone(data.PHONE_MIN_LENGTH_10)

        assert self.page.get_phone_border_color() == data.VALID_BORDER_COLOR

    # ---------- JSQ-4: Phone with 13 chars is accepted (should be rejected) ----------
    @pytest.mark.xfail(
        reason="BUG JSQ-4: phone with 13 characters is accepted, should be rejected (max 12)"
    )
    def test_phone_above_max_length_should_be_rejected(self):
        self.page.set_phone(data.PHONE_ABOVE_MAX_13)

        assert self.page.get_phone_border_color() == data.INVALID_BORDER_COLOR

    # ---------- JSQ-11: First/Last name do not trim leading/trailing spaces ----------
    @pytest.mark.xfail(reason="BUG JSQ-11: leading/trailing spaces in name are not trimmed")
    def test_first_name_should_trim_spaces(self):
        self.page.set_first_name("  Maria  ")

        assert self.page.get_first_name_value() == "Maria"

    # ---------- JSQ-6: Cookie banner does not disappear ----------
    @pytest.mark.xfail(reason="BUG JSQ-6: cookie banner stays visible even after accepting")
    def test_cookie_banner_should_disappear_after_accept(self):
        self.page.accept_cookies_if_present()

        assert not self.page.is_cookie_banner_visible()

    # ---------- Success case (no bug): valid data is accepted ----------
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
