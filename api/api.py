import requests
from data.data import *
import json


def get_track_number():
    order_data = json.dumps(DataToCreateOrder.payload)
    response = requests.post(OrdersLinks.orders, data=order_data)
    track_number = response.json()["track"]
    return track_number


def get_order_id_by_track_number():
    params = {"t": get_track_number()}
    response = requests.get(OrdersLinks.track_order, params=params)
    return response.json()["order"]["id"]
