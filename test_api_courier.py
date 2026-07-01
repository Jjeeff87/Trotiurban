import requests
import pytest

import data
import helpers


def create_courier(login, password, first_name=None):
    payload = {"login": login, "password": password}
    if first_name is not None:
        payload["firstName"] = first_name
    return requests.post(f"{data.API_BASE_URL}/api/v1/courier", json=payload)


def login_courier(login, password):
    return requests.post(
        f"{data.API_BASE_URL}/api/v1/courier/login",
        json={"login": login, "password": password},
    )


def delete_courier(courier_id):
    return requests.delete(f"{data.API_BASE_URL}/api/v1/courier/{courier_id}")


@pytest.fixture(scope="module", autouse=True)
def check_server():
    assert helpers.is_url_reachable(f"{data.API_BASE_URL}/api/v1/ping"), (
        "Servidor da API não está acessível. Verifique se está ligado e "
        "atualize API_BASE_URL em data.py"
    )


class TestCreateCourier:
    """POST /api/v1/courier — Adicionar entregador."""

    def test_valid_data_creates_courier(self):
        response = create_courier(helpers.unique_login(), data.VALID_PASSWORD, "Ana")
        assert response.status_code == 201

    def test_missing_login_returns_400(self):
        response = requests.post(
            f"{data.API_BASE_URL}/api/v1/courier",
            json={"password": data.VALID_PASSWORD, "firstName": "Ana"},
        )
        assert response.status_code == 400

    def test_missing_password_returns_400(self):
        response = requests.post(
            f"{data.API_BASE_URL}/api/v1/courier",
            json={"login": helpers.unique_login(), "firstName": "Ana"},
        )
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-13: firstName ausente não é validado (deveria retornar 400)")
    def test_missing_first_name_returns_400(self):
        response = create_courier(helpers.unique_login(), data.VALID_PASSWORD)
        assert response.status_code == 400

    def test_empty_body_returns_400(self):
        response = requests.post(f"{data.API_BASE_URL}/api/v1/courier", json={})
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-12: login com números não é validado")
    def test_login_with_numbers_is_rejected(self):
        response = create_courier("abc123" + helpers.unique_login(), data.VALID_PASSWORD, "Ana")
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-12: login com caractere especial não é validado")
    def test_login_with_special_char_is_rejected(self):
        response = create_courier("ab@cd" + helpers.unique_login(), data.VALID_PASSWORD, "Ana")
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-12: login com 1 caractere (abaixo do mínimo) não é validado")
    def test_login_below_min_length_is_rejected(self):
        response = create_courier("a", data.VALID_PASSWORD, "Ana")
        assert response.status_code == 400

    def test_login_at_min_length_2_is_accepted(self):
        response = create_courier(helpers.unique_login()[:2], data.VALID_PASSWORD, "Ana")
        assert response.status_code in (201, 409)

    def test_login_at_max_length_10_is_accepted(self):
        response = create_courier(helpers.unique_login()[:10].rjust(10, "x"), data.VALID_PASSWORD, "Ana")
        assert response.status_code in (201, 409)

    @pytest.mark.xfail(reason="BUG JSQ-12: login com 11 caracteres (acima do máximo) não é validado")
    def test_login_above_max_length_is_rejected(self):
        response = create_courier("abcdefghijk", data.VALID_PASSWORD, "Ana")
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-14: firstName com números não é validado")
    def test_first_name_with_numbers_is_rejected(self):
        response = create_courier(helpers.unique_login(), data.VALID_PASSWORD, "Ana123")
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-14: firstName fora do limite de tamanho não é validado")
    def test_first_name_below_min_length_is_rejected(self):
        response = create_courier(helpers.unique_login(), data.VALID_PASSWORD, "A")
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-15: password com letras não é validado")
    def test_password_with_letters_is_rejected(self):
        response = create_courier(helpers.unique_login(), "abcd", "Ana")
        assert response.status_code == 400

    @pytest.mark.xfail(reason="BUG JSQ-15: password com tamanho diferente de 4 não é validado")
    def test_password_wrong_length_is_rejected(self):
        response = create_courier(helpers.unique_login(), "123", "Ana")
        assert response.status_code == 400

    def test_duplicate_login_returns_409(self):
        login = helpers.unique_login()
        create_courier(login, data.VALID_PASSWORD, "Ana")
        response = create_courier(login, data.VALID_PASSWORD, "Outro")
        assert response.status_code == 409


class TestDeleteCourier:
    """DELETE /api/v1/courier/:id — Excluir entregador."""

    @staticmethod
    def _create_and_login():
        login = helpers.unique_login("del")
        create_courier(login, data.VALID_PASSWORD, "Excluir")
        courier_id = login_courier(login, data.VALID_PASSWORD).json()["id"]
        return login, courier_id

    def test_delete_existing_courier_returns_200(self):
        _, courier_id = self._create_and_login()
        response = delete_courier(courier_id)
        assert response.status_code == 200

    @pytest.mark.xfail(reason="BUG JSQ-16: pedidos vinculados não são apagados ao excluir o entregador")
    def test_delete_courier_removes_linked_orders(self):
        login, courier_id = self._create_and_login()

        order = requests.post(
            f"{data.API_BASE_URL}/api/v1/orders",
            json={
                "firstName": "Cliente", "lastName": "Teste", "address": "Rua X, 100",
                "metroStation": "Sé", "phone": "+551199999999", "rentTime": 3,
                "deliveryDate": "2026-07-05", "comment": "teste cascade", "color": ["black"],
            },
        ).json()
        track = order["track"]

        order_data = requests.get(f"{data.API_BASE_URL}/api/v1/orders/track", params={"t": track}).json()
        order_id = order_data["order"]["id"]
        requests.put(f"{data.API_BASE_URL}/api/v1/orders/accept/{order_id}", params={"courierId": courier_id})

        delete_courier(courier_id)

        response = requests.get(f"{data.API_BASE_URL}/api/v1/orders/track", params={"t": track})
        assert response.status_code == 404

    def test_delete_nonexistent_courier_returns_404(self):
        response = delete_courier(999999)
        assert response.status_code == 404

    @pytest.mark.xfail(reason="BUG JSQ-17: ID inválido retorna 500 com erro interno exposto, deveria ser 400")
    def test_delete_with_invalid_id_format_returns_400(self):
        response = delete_courier("abc")
        assert response.status_code == 400

    def test_delete_already_deleted_courier_returns_404(self):
        _, courier_id = self._create_and_login()
        delete_courier(courier_id)
        response = delete_courier(courier_id)
        assert response.status_code == 404

    def test_login_fails_after_courier_deleted(self):
        login, courier_id = self._create_and_login()
        delete_courier(courier_id)
        response = login_courier(login, data.VALID_PASSWORD)
        assert response.status_code == 404
