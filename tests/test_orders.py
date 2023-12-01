import pytest
import allure
import requests
import helpers
from data.data import *
import json
from api import api


class TestGetOrders:

    @allure.title("Получение списка заказов")
    @allure.description('Проверка успешного получения списка заказов без дополнительных параметров')
    def test_get_orders_list_success(self):
        response = requests.get(OrdersLinks.orders)
        orders_list = response.json()["orders"]
        assert type(orders_list) == list

    @allure.title("Получение заказа без трек-номера или с несуществующим трек-номером")
    @allure.description('Проверка возможности получения заказа без трек-номера или с несуществующим трек-номером')
    @pytest.mark.parametrize('track_number, answer', [[helpers.random_track_number(), 404], ["", 400]])
    def test_get_order_by_track_number_fail(self, track_number, answer):
        params = {}
        params["t"] = [track_number]
        response = requests.get(OrdersLinks.track_order, params=params)
        assert response.status_code == answer

    @allure.title("Получение заказа по его трек-номерому")
    @allure.description('Проверка возможности получения заказа по его трек-номерому')
    def test_get_order_by_track_number_positive(self):
        params = {"t": api.get_track_number()}
        response = requests.get(OrdersLinks.track_order, params=params)
        assert "order" in response.text


class TestCreateOrder:
    @allure.title("Создание заказа")
    @allure.description(
        'Проверка возможности создания заказа с указанием одного или двух цветов (BLACK или GREY), либо без указания цвета')
    @pytest.mark.parametrize('color', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_orders_list_success(self, color):
        DataToCreateOrder.payload["color"] = [color]
        order_data = json.dumps(DataToCreateOrder.payload)
        response = requests.post(OrdersLinks.orders, data=order_data)
        assert 'track' in response.text
