import requests
import random
import string
from data.data import *
import json


def credentials_generator():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)


    credentials = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return credentials


def no_login_courier():
    reg = credentials_generator()
    reg.pop('login')
    return reg


def no_password_courier():
    reg = credentials_generator()
    reg.pop('password')
    return reg


def empty_login_courier():
    reg = credentials_generator()
    reg.update({'login':''})
    return reg


def empty_password_courier():
    reg = credentials_generator()
    reg.update({'password':''})
    return reg

def random_login_data():
    reg = credentials_generator()
    reg.pop('firstName')
    return reg

def random_track_number():
    track_number = random.randint(9000000,9999999)
    return track_number
print(random_track_number())


def get_track_number():
    order_data = json.dumps(DataToCreateOrder.payload)
    response = requests.post(OrdersLinks.orders, data=order_data)
    track_number = response.json()["track"]
    return track_number

def get_order_id_by_track_number():
    params = {"t": get_track_number()}
    response = requests.get(OrdersLinks.track_order, params=params)
    return response.json()["order"]["id"]


