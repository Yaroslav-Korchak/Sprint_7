import pytest
import allure
import requests
import helpers
from data.data import *
import random
import string
from api import api


class TestCourier:

    # @classmethod
    # def create_courier(cls):
    #     def generate_random_string(length):
    #         letters = string.ascii_lowercase
    #         random_string = ''.join(random.choice(letters) for i in range(length))
    #         return random_string
    #
    #     login = generate_random_string(10)
    #     password = generate_random_string(10)
    #     first_name = generate_random_string(10)
    #
    #     payload = {
    #         "login": login,
    #         "password": password,
    #         "firstName": first_name
    #     }
    #     response = requests.post(TestCourierLinks.courier_url, data=payload)
    #
    #     return response, payload
    # @staticmethod
    # def return_login_data():
    #     payload = TestCourier.create_courier()
    #     data = payload[1]
    #     login_data = data
    #     login_data.pop("firstName")
    #     return login_data

    @allure.title('Создание курьера. Позитивный сценарий')
    @allure.description('Проверка создания курьера через метод класса')
    def test_create_courier_positive(self, create_courier):
        status = create_courier[0]
        assert status.status_code == 201 and status.text == '{"ok":true}'

    @allure.title('Создание дубликата курьера')
    @allure.description('Проверка создания курьера с использованием уже зарегистрированного логина и пароля')
    def test_create_courier_positive_duplicate(self, create_courier):
        login_data = create_courier[2]
        response = requests.post(TestCourierLinks.courier_url, data=login_data)
        assert response.status_code == 409 and response.json()['message'] == "Этот логин уже используется. Попробуйте другой."


    @allure.title('Создание курьера без обязательных данных')
    @allure.description('Проверка создания курьера обязательных строк, или с пустыми значениями в них')
    @pytest.mark.parametrize('payload', [helpers.no_login_courier(), helpers.no_password_courier(), helpers.empty_login_courier(),
                helpers.empty_password_courier()])
    def test_create_courier_without_mandatory_data(self, payload):
        r = requests.post(TestCourierLinks.courier_url, data=payload)

        assert r.status_code == 400 and r.json()['message'] == "Недостаточно данных для создания учетной записи"


    # В данном тесте, если отправить тело без пароля или "password": null, где-то через минуту от сервера приходит ошибка 504 Service unavailable
    # Наставник сказала что это баг и оставить так, и добавить комментарий в код. Так что как-то так)

    @allure.title('Авторизация курьера без обязательных данных')
    @allure.description('Проверка возможности войти в учётную запись курьера без обязательных строк, или с пустыми значениями в них')
    @pytest.mark.parametrize('payload', [EmptyPartOfCredentials.only_password,
                                         EmptyPartOfCredentials.empty_login,
                                         EmptyPartOfCredentials.empty_password,
                                         EmptyPartOfCredentials.only_login])
    def test_login_courier_without_mandatory_data(self, payload):
        r = requests.post(TestCourierLinks.login_url, data=payload)
        assert r.status_code == 400 and r.json()['message'] == "Недостаточно данных для входа"

    @allure.title('Авторизация курьера с несуществующими данными')
    @allure.description(
        'Проверка возможности войти в учётную запись курьера с использованием несуществующих данных')
    def test_login_courier_with_wrong_data(self):
        r = requests.post(TestCourierLinks.login_url, data=helpers.random_login_data())
        assert r.status_code == 404 and r.json()['message'] == "Учетная запись не найдена"

    @allure.title('Авторизация курьера с существующими данными')
    @allure.description('Проверка возможности войти в учётную запись курьера с использованием существующих данных')
    def test_login_courier_with_existing_data(self):
        r = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        assert r.status_code == 200 and len(str(r.json()['id'])) > 0

    @allure.title('Принять заказ')
    @allure.description('Проверка успешного принятия заказа при отправке всех корректных данных')
    def test_accept_order_successful(self):
        r = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        courier_id = (r.json()['id'])
        params = {'courierId': courier_id}
        response = requests.put(OrdersLinks.accept_order + str(api.get_order_id_by_track_number()), params=params)
        assert response.text == '{"ok":true}' and response.status_code == 200

    @allure.title('Принять заказ без id курьера')
    @allure.description('Попытка принять заказ без id курьера должна вернуть ошибку 400')
    def test_accept_order_without_courier_id_fail(self):
        response = requests.put(OrdersLinks.accept_order + str(api.get_order_id_by_track_number()))
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для поиска"


    @allure.title('Принять заказ с несуществующим id курьера')
    @allure.description('Попытка принять заказ с несуществующим id курьера должна вернуть ошибку 404')
    def test_accept_order_with_wrong_courier_id(self):
        r = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        courier_id = (r.json()['id']) + random.randint(10000, 99999)
        params = {'courierId': courier_id}
        response = requests.put(OrdersLinks.accept_order + str(api.get_order_id_by_track_number()), params=params)
        assert response.status_code == 404 and response.json()['message'] == "Курьера с таким id не существует"

    @allure.title('Принять заказ с несуществующим id заказа')
    @allure.description('Попытка принять заказ с несуществующим id заказа должна вернуть ошибку 404')
    def test_accept_order_with_wrong_order_id(self):
        r = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        courier_id = r.json()['id']
        params = {'courierId': courier_id}
        response = requests.put(OrdersLinks.accept_order + str(api.get_order_id_by_track_number() + random.randint(10000, 99999)),
                                params=params)
        assert response.status_code == 404 and response.json()['message'] == "Заказа с таким id не существует"

    @allure.title('Принять заказ без id заказа')
    @allure.description('Попытка принять заказ без id заказа должна вернуть ошибку 400')
    def test_accept_order_without_order_id_fail(self):
        r = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        courier_id = (r.json()['id'])
        params = {'courierId': courier_id}
        response = requests.put(OrdersLinks.accept_order,  params=params)
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для поиска"

    @allure.title('Удаление курьера без отправки id')
    @allure.description('Проверка удаления курьера без отправки id')
    def test_delete_courier_positive(self):
        r = requests.delete(TestCourierLinks.delete_courier_url)
        assert r.status_code == 400 and r.json()['message'] == 'Недостаточно данных для удаления курьера'

    @allure.title('Удаление курьера с несуществующим id')
    @allure.description('Проверка удаления курьера с несуществующим id')
    def test_delete_courier_positive(self):
        response = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        courier_id = response.json()["id"]
        r = requests.delete(TestCourierLinks.delete_courier_url + str(courier_id + random.randint(10000, 99999)))
        assert r.status_code == 404 and r.json()['message'] == '"Курьера с таким id нет.'

    @allure.title('Удаление курьера')
    @allure.description('Проверка удаления курьера позитивный сценарий')
    def test_delete_courier_positive(self):
        response = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        courier_id = response.json()["id"]
        r = requests.delete(TestCourierLinks.delete_courier_url + str(courier_id))
        assert r.status_code == 200 and r.text == '{"ok":true}'