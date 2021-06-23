from django.http import HttpResponse
import json
from .models import ORDER, BPLA, HUB
import datetime
from .requests import calculate_order_route, send_order_to_first_hub


def index(request):
    return HttpResponse("<h1>Hello, world!</h1>")


def manage_orders(request):
    if request.method == "POST":  # Обработка запроса на создание нового заказа
        new_order_data = request.POST
        # Запрос на построение маршрута
        math_module_answer = calculate_order_route(new_order_data.weight, new_order_data.first_hub, new_order_data.last_hub)
        track = str(math_module_answer)
        # Запись в БД
        new_order = ORDER(weight=new_order_data.weight,
                          cur_departure=new_order_data.first_hub,
                          cur_destination=math_module_answer["Product_path"][1]["HubID"],
                          bpla=None,
                          track=track,
                          start_time=datetime.now())
        new_order.save()
        # Передача заказа в Хаб
        send_order_to_first_hub(new_order_data.first_hub, new_order.id)
        return HttpResponse("<h1>Success</h1>")
    else:
        return HttpResponse("<h1>Inappropriate request type.</h1>")


def manage_drone(request, drone_id):
    if request.method == "UPDATE":
        drone_data = request.UPDATE
        drone = BPLA.objects.filter(id=drone_id)
        drone.speed = drone_data.speed
        drone.latitude = drone_data.latitude
        drone.longitude = drone_data.longitude
        drone.azimuth = drone_data.azimuth
        drone.save()
        return HttpResponse("<h1>Success</h1>")


def update_order(request, order_id):
    if request.method == "UPDATE":
        order_data = request.UPDATE
        order = ORDER.objects.filter(id=order_id)
        order.bpla = order_data.bpla
        order.cur_departure = order_data.hub_id
        if order_data.dest_hub_id is not None:
            order.cur_destination = order_data.dest_hub_id
        # Добавить информацию об окончании заказа
        order.save()
        return HttpResponse("<h1>Success</h1>")
    elif request.method == "GET":
        order = ORDER.objects.filter(id=order_id)
        order_json = {"weight": order.weight,
                      "cur_departure": order.cur_departure,
                      "cur_destination": order.cur_destination,
                      "bpla": order.bpla,
                      "track": order.track,
                      "start_time": order.start_time}
        order_json = json.dumps(order_json)
        return HttpResponse(order_json, content_type="application/json")

def get_drone_locations(request):
    if request.method == "GET":
        screen_data = request.GET
        drones = BPLA.objects.filter(latitude__gte=screen_data.less_latitude
                                     ).filter(latitude__lte=screen_data.more_latitude
                                     ).filter(longitude__gte=screen_data.less_longitude
                                     ).filter(longitude__lte=screen_data.more_longitude)
        drone_data = dict()
        for drone in drones:
            drone_data.update({drone.id: [drone.latitude, drone.longitude, drone.speed, drone.azimuth]})
        drone_data = json.dumps(drone_data)
        return HttpResponse(drone_data, content_type="application/json")


def manage_graph(request):
    if request.method == "POST":
        new_hub_data = request.POST
        new_hub = HUB(type=new_hub_data.type,
                      workload=new_hub_data.workload,
                      latitude=new_hub_data.latitude,
                      longitude=new_hub_data.longitude)
        new_hub.save()
        return HttpResponse("<h1>Success</h1>")
    elif request.method == "DELETE":
        hub_data = request.DELETE
        HUB.objects.filter(id=hub_data.hub_id).delete()
        return HttpResponse("<h1>Success</h1>")
