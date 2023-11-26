import pytest
import allure
import requests
import helpers
from data.data import *
import random
import string
import json

class TestOrders:

    @allure.description("Получение списка заказов")
    @allure.title('Проверка успешного получения списка заказов без дополнительных параметров')
    def test_get_orders_list_success(self):
        response = requests.get(OrdersLinks.orders)
        orders_list = response.json()["orders"]
        assert type(orders_list) == list

    @allure.description("Создание заказа")
    @allure.title('Проверка возможности создания заказа с указанием одного или двух цветов (BLACK или GREY), либо без указания цвета')
    @pytest.mark.parametrize('color', [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_orders_list_success(self, color):
        DataToCreateOrder.payload["color"] = [color]
        order_data = json.dumps(DataToCreateOrder.payload)
        response = requests.post(OrdersLinks.orders, data=order_data)
        assert response.status_code == 201 and 'track' in response.text



