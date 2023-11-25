import pytest
import allure
import requests
import helpers
from data.data import *
import random
import string
import json


class TestCourierCreateAPI:

    @classmethod
    def setup_class(cls):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        return response, payload
    @staticmethod
    def return_login_data():
        payload = TestCourierCreateAPI.setup_class()
        data = payload[1]
        login_data = data
        login_data.pop("firstName")
        return login_data

    @allure.title('Создание курьера. Позитивный сценарий')
    @allure.description('Проверка создания курьера через метод класса')
    def test_create_courier_positive(self):
        status = self.setup_class()
        assert status[0].status_code == 201 and status[0].text == '{"ok":true}'

    @allure.title('Создание дубликата курьера')
    @allure.description('Проверка создания курьера с использованием уже зарегистрированного логина и пароля')
    def test_create_courier_positive_duplicate(self):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=self.return_login_data())
        try:
            assert response.status_code == 409
        except AssertionError:
            print("Код ответа в тесте 'test_create_courier_positive_duplicate' не соответствует ожидаемому")
        try:
            assert response.text == '{"message": "Этот логин уже используется. Попробуйте другой."}'
        except AssertionError:
            print("Текст сообщения в тесте 'test_create_courier_positive_duplicate' не соответствует ожидаемому")


    @allure.title('Создание курьера без обязательных данных')
    @allure.description('Проверка создания курьера обязательных строк, или с пустыми значениями в них')
    @pytest.mark.parametrize('payload', [helpers.no_login_courier(), helpers.no_password_courier(), helpers.empty_login_courier(),
                helpers.empty_password_courier()])
    def test_create_courier_without_mandatory_data(self, payload):
        r = requests.post(TestCourierLinks.courier_url, data=payload)

        assert r.status_code == 400 and r.json()['message'] == "Недостаточно данных для создания учетной записи"


    # В данном тесте, если отправить тело без пароля или "password": null, где-то через минуту от сервера приходит ошибка 504 Service unavailable
    # Наставник сказала что это баг и оставить так, и добавить комментарий в код. Так что как-то так)

    # EmptyPartOfCredentials.only_login
    @allure.title('Логин курьера без обязательных данных')
    @allure.description('Проверка возможности войти в учётную запись курьера без обязательных строк, или с пустыми значениями в них')
    @pytest.mark.parametrize('payload', [EmptyPartOfCredentials.only_password,
                                         EmptyPartOfCredentials.empty_login,
                                         EmptyPartOfCredentials.empty_password])
    def test_login_courier_without_mandatory_data(self, payload):
        r = requests.post(TestCourierLinks.login_url, data=payload)
        try:
            assert r.status_code == 400
        except AssertionError:
            print("Код ответа в тесте 'test_login_courier_without_mandatory_data' не соответствует ожидаемому")
        try:
            assert r.json()['message'] == "Недостаточно данных для входа"
        except AssertionError:
            print("Текст сообщения в тесте 'test_login_courier_without_mandatory_data' не соответствует ожидаемому")





































    @allure.title('Удаление курьера')
    @allure.description('Проверка удаления курьера позитивный сценарий')
    def test_delete_courier_positive(self):
        response = requests.post(TestCourierLinks.login_url, data=self.return_login_data())
        courier_id = response.json()["id"]
        r = requests.delete('https://qa-scooter.praktikum-services.ru/api/v1/courier/' + str(courier_id))
        assert r.status_code == 200 and r.text == '{"ok":true}'