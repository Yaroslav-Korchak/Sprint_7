import allure
import requests
from data.data import *
import random
from api import api


class TestOrdersAccept:
    @allure.title('Принять заказ')
    @allure.description('Проверка успешного принятия заказа при отправке всех корректных данных')
    def test_accept_order_successful(self, create_and_delete_courier):
        r = requests.post(TestCourierLinks.login_url, data=create_and_delete_courier[2])
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
    def test_accept_order_with_wrong_courier_id(self, create_and_delete_courier):
        r = requests.post(TestCourierLinks.login_url, data=create_and_delete_courier[2])
        courier_id = (r.json()['id']) + random.randint(10000, 99999)
        params = {'courierId': courier_id}
        response = requests.put(OrdersLinks.accept_order + str(api.get_order_id_by_track_number()), params=params)
        assert response.status_code == 404 and response.json()['message'] == "Курьера с таким id не существует"


    @allure.title('Принять заказ с несуществующим id заказа')
    @allure.description('Попытка принять заказ с несуществующим id заказа должна вернуть ошибку 404')
    def test_accept_order_with_wrong_order_id(self, create_and_delete_courier):
        r = requests.post(TestCourierLinks.login_url, data=create_and_delete_courier[2])
        courier_id = r.json()['id']
        params = {'courierId': courier_id}
        response = requests.put(
            OrdersLinks.accept_order + str(api.get_order_id_by_track_number() + random.randint(10000, 99999)),
            params=params)
        assert response.status_code == 404 and response.json()['message'] == "Заказа с таким id не существует"


    @allure.title('Принять заказ без id заказа')
    @allure.description('Попытка принять заказ без id заказа должна вернуть ошибку 400')
    def test_accept_order_without_order_id_fail(self, create_and_delete_courier):
        r = requests.post(TestCourierLinks.login_url, data=create_and_delete_courier[2])
        courier_id = (r.json()['id'])
        params = {'courierId': courier_id}
        response = requests.put(OrdersLinks.accept_order, params=params)
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для поиска"