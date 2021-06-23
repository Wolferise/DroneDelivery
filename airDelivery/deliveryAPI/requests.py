import requests
from .models import HUB


def calculate_order_route(weight, first_hub, last_hub):
    url = "<SERVER_IP>/api/orders"
    order_data = {{'weight': weight, 'first_hub': first_hub, 'last_hub': last_hub}}
    track = requests.post(url, json=order_data)
    return track


def send_order_to_first_hub(first_hub, order_id):
    hub_ip = HUB.objects.filter(id=first_hub).ip
    url = hub_ip + "/api/orders"
    order_data = {'order_id': order_id}
    requests.post(url, json=order_data)
