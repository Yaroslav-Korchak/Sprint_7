class TestCourierLinks:
    courier_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/'
    login_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'


class EmptyPartOfCredentials:
    only_login = {"login": "fake_person"}
    only_password = {"password": "fake_password"}
    empty_login = {"login": "", "password": "fake_password"}
    empty_password = {"login": "fake_person", "password": ""}


class OrdersLinks:
    orders = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    track_order = 'https://qa-scooter.praktikum-services.ru/api/v1/orders/track'



class DataToCreateOrder:
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha"
    }

