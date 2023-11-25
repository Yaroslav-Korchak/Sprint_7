class TestCourierLinks:
    courier_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/'
    login_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'


class EmptyPartOfCredentials:
    only_login = {"login": "fake_person"}
    only_password = {"password": "fake_password"}
    empty_login = {"login": "", "password": "fake_password"}
    empty_password = {"login": "fake_person", "password": ""}
