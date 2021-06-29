import requests
import json
from .models import HUB


def calculate_order_route(weight, first_hub, last_hub):
    url = "http://192.168.1.221/api/orders"
    order_data = {'weight': float(weight), 'first_hub': int(first_hub), 'last_hub': int(last_hub)}
    order_data = json.dumps(order_data)
    print(order_data, type(order_data))
    track = requests.post(url, json=order_data)
    return track


def send_order_to_first_hub(first_hub, order_id):
    hub_ip = HUB.objects.filter(id=first_hub).ip
    url = hub_ip + "/api/orders"
    order_data = {'order_id': int(order_id)}
    order_data = json.dumps(order_data)
    requests.post(url, json=order_data)
