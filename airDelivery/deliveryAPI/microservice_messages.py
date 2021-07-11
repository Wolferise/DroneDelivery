import requests
import json

math_module_url = "http://26.108.74.21"
math_module_port = "80"
hub_url = "http://26.108.74.21"
hub_base_port = "8000"


def get_order_track_from_math_module(order_weight, departure_point, destination_point):
    request_url = math_module_url + ":" + math_module_port
    request_body = {'weight': float(order_weight), 'first_hub': int(departure_point), 'last_hub': int(destination_point)}
    result = json.loads(requests.post(request_url, data=request_body).content)
    return result


def start_shipping_message(hub_id, order_id, track):
    port = str(int(hub_base_port) + int(hub_id))
    request_url = hub_url + ":" + port + "/api/orders"
    request_body = {'order_id': int(order_id), 'order_track': track}
    requests.post(request_url, json=request_body)