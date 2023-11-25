import requests
import random
import string
from data.data import *


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
    reg.pop('password')
    return reg


def no_password_courier():
    reg = credentials_generator()
    reg.pop('login')
    return reg


def empty_login_courier():
    reg = credentials_generator()
    reg.update({'login':''})
    return reg


def empty_password_courier():
    reg = credentials_generator()
    reg.update({'password':''})
    return reg
