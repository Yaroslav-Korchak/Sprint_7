import pytest
import allure
import requests
import helpers
from data.data import *
import random


class TestCourier:

    @allure.title('Создание курьера. Позитивный сценарий')
    @allure.description('Проверка создания курьера через метод класса')
    def test_create_courier_positive(self, create_and_delete_courier):
        status = create_and_delete_courier[0]
        assert status.status_code == 201 and status.text == '{"ok":true}'

    @allure.title('Создание дубликата курьера')
    @allure.description('Проверка создания курьера с использованием уже зарегистрированного логина и пароля')
    def test_create_courier_positive_duplicate(self, create_and_delete_courier):
        response = requests.post(TestCourierLinks.courier_url, data=create_and_delete_courier[2])
        assert response.status_code == 409 and response.json()['message'] == ("Этот логин уже используется."
                                                                              " Попробуйте другой.")

    @allure.title('Создание курьера без обязательных данных')
    @allure.description('Проверка создания курьера обязательных строк, или с пустыми значениями в них')
    @pytest.mark.parametrize('payload', [helpers.no_login_courier(), helpers.no_password_courier(),
                                         helpers.empty_login_courier(), helpers.empty_password_courier()])
    def test_create_courier_without_mandatory_data(self, payload):
        r = requests.post(TestCourierLinks.courier_url, data=payload)

        assert r.status_code == 400 and r.json()['message'] == "Недостаточно данных для создания учетной записи"


class TestCourierLogin:

    # В данном тесте, если отправить тело без пароля или "password": null,
    # где-то через минуту от сервера приходит ошибка 504 Service unavailable
    # Наставник сказала что это баг и оставить так, и добавить комментарий в код. Так что как-то так)

    @allure.title('Авторизация курьера без обязательных данных')
    @allure.description('Проверка возможности войти в учётную запись'
                        ' курьера без обязательных строк, или с пустыми значениями в них')
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
    def test_login_courier_with_existing_data(self, create_and_delete_courier):
        r = requests.post(TestCourierLinks.login_url, data=create_and_delete_courier[2])
        assert r.status_code == 200 and len(str(r.json()['id'])) > 0


class TestCourierDelete:

    @allure.title('Удаление курьера без отправки id')
    @allure.description('Проверка удаления курьера без отправки id')
    def test_delete_courier_without_id(self):
        r = requests.delete(TestCourierLinks.delete_courier_url)
        assert r.status_code == 400 and r.json()['message'] == 'Недостаточно данных для удаления курьера'

    @allure.title('Удаление курьера с несуществующим id')
    @allure.description('Проверка удаления курьера с несуществующим id')
    def test_delete_courier_with_wrong_id(self, create_and_delete_courier):
        response = requests.post(TestCourierLinks.login_url, data=create_and_delete_courier[2])
        courier_id = response.json()["id"]
        r = requests.delete(TestCourierLinks.delete_courier_url + str(courier_id + random.randint(10000, 99999)))
        assert r.status_code == 404 and r.json()['message'] == 'Курьера с таким id нет.'

    @allure.title('Удаление курьера')
    @allure.description('Проверка удаления курьера позитивный сценарий')
    def test_delete_courier_positive(self):
        payload = helpers.random_login_data()
        requests.post(TestCourierLinks.courier_url, data=payload)
        response = requests.post(TestCourierLinks.login_url, data=payload)
        courier_id = response.json()["id"]
        r = requests.delete(TestCourierLinks.delete_courier_url + str(courier_id))
        assert r.status_code == 200 and r.text == '{"ok":true}'