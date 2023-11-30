import pytest
import allure
import requests
from data.data import *
import random
import string


@pytest.fixture
def create_courier():
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

    login_data = payload
    login_data.pop("firstName")
    response = requests.post(TestCourierLinks.courier_url, data=payload)

    return response, payload, login_data
