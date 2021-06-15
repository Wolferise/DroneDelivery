from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import ORDER, BPLA
import datetime
from .requests import calculate_order_route, send_order_to_first_hub
# Create your views here.


def index(request):
    return HttpResponse("<h1>Hello, world!</h1>")


def manage_orders(request):
    if request.method == "POST":  # Обработка запроса на создание нового заказа
        new_order_data = request.POST
        # Запрос на построение маршрута
        track = calculate_order_route(new_order_data.weight, new_order_data.first_hub, new_order_data.last_hub)
        # Запись в БД
        new_order = ORDER(weight=new_order_data.weight,
                          cur_departure=1,  # Удалить из БД
                          cur_destination=2,  # Удалить из БД
                          bpla=3,  # Удалить из БД
                          track=track,
                          start_time=datetime.now())
        new_order.save()
        # Передача заказа в Хаб
        send_order_to_first_hub(new_order_data.first_hub, new_order.id)
        return HttpResponse("<h1>Success</h1>")
    elif request.method == "GET":  # Обработка запроса на получение данных по всем заказам
        # Взаимодействие с БД
        db_orders = ORDER.objects.all()
        orders_data = {
            'some_var_1': 'foo',
            'some_var_2': 'bar',
        }
        orders = json.dumps(orders_data)
        return HttpResponse(orders, content_type='application/json')


def manage_drone(request, drone_id):
    if request.method == "UPDATE":
        drone_data = request.UPDATE
        drone = BPLA.objects.filter(id=drone_id)
        drone.speed = drone_data.speed
        drone.latitude = drone_data.latitude
        drone.longitude = drone_data.longitude
        drone.azimuth = drone_data.azimuth
        drone.save()


def order_update(request, order_id):
    if request.method == "UPDATE":
        pass


def get_drone_locations(request):
    if request.method == "GET":
        pass
