from django.http import HttpResponse
import json
from .models import ORDER, BPLA, HUB
import ast
from . import microservice_messages as messages
from django.views.decorators.csrf import csrf_exempt
from . import db_interactions as database


def manage_orders(request):

    # Добавление нового заказа
    if request.method == "POST":
        order_params = request.GET

        # Построение маршрута заказа математическим модулем
        track = messages.get_order_track_from_math_module(order_params['weight'],
                                                          order_params['first_hub'],
                                                          order_params['last_hub'])

        # Запись заказа в БД
        new_order = database.create_order(order_params, track)

        # Передача данных о заказе для дальнейшей обработки другими модулями
        messages.start_shipping_message(new_order.cur_departure, new_order.id, new_order.track)
        return HttpResponse("<h1>Successfully started shipping.</h1>")


@csrf_exempt
def manage_single_order(request, order_id):

    # Обновление данных по конкретному заказу
    if request.method == "PUT":
        order_data = ast.literal_eval(json.loads(request.read().decode('utf-8')))
        try:
            order = ORDER.objects.get(id=order_id)
        except IndexError:
            for order in ORDER.objects.all():
                print(order.id)
        order.bpla = BPLA.objects.get(board_number=str(order_data['bpla']))
        order.cur_departure = HUB.objects.get(hub_id=(int(order_data['dep_hub_id'])))
        if order_data['dest_hub_id'] is not None:
            order.cur_destination = HUB.objects.get(hub_id=(int(order_data['dest_hub_id'])))
        order.save()
        return HttpResponse("<h1>Successfully added new order data to DB.</h1>")

    # Отправка данных по конкретному заказу
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


@csrf_exempt
def manage_drone_fleet(request):

    # Передача данных о текущих параметрах всех беспилотных аппаратов, находящихся в воздухе в данный момент
    if request.method == "GET":
        drone_fleet = BPLA.objects.all()
        drone_fleet_params = dict()
        for uav in drone_fleet:
            drone_fleet_params.update({int(uav.id): {'id': uav.id,
                                                     'lat': uav.latitude,
                                                     'lon': uav.longitude,
                                                     'speed': uav.speed,
                                                     'azimuth': uav.azimuth}})
        return HttpResponse(json.dumps(drone_fleet_params), content_type="application/json")

    # Добавление нового беспилотного аппарата в БД
    elif request.method == "POST":
        uav_params = request.POST
        database.create_uav(uav_params)
        return HttpResponse("<h1>Successfully added new UAV</h1>")

    # Удаление всех беспилотных аппаратов, находящихся в воздухе в данный момент
    elif request.method == "DELETE":
        BPLA.objects.all().delete()
        return HttpResponse("<h1>Successfully erased all active UAVs.</h1>")

    # Обновление параметров всех находящихся в работе в данный момент времени беспилотных аппаратов
    elif request.method == "PUT":
        uav_updated_params = ast.literal_eval(request.body.decode('utf-8'))
        for uav in BPLA.objects.all():
            uav.speed = uav_updated_params[uav.id]['speed']
            uav.latitude = uav_updated_params[uav.id]['latitude']
            uav.longitude = uav_updated_params[uav.id]['longitude']
            uav.azimuth = uav_updated_params[uav.id]['azimuth']
            uav.save()
        return HttpResponse("<h1>Successfully updated all uav data.</h1>")


@csrf_exempt
def manage_single_uav(request, uav_id):

    # Обовление параметров конкретного беспилотного аппарата
    if request.method == "PUT":
        uav_updated_params = ast.literal_eval(request.body.decode('utf-8'))
        uav = BPLA.objects.get(id=uav_id)
        uav.speed = uav_updated_params['speed']
        uav.latitude = uav_updated_params['latitude']
        uav.longitude = uav_updated_params['longitude']
        uav.azimuth = uav_updated_params['azimuth']
        uav.save()
        return HttpResponse("<h1>Successfully updated uav data.</h1>")

    # Удаление конкретного беспилотного аппарата
    elif request.method == "DELETE":
        uav = BPLA.objects.get(id=uav_id)
        uav.delete()
        return HttpResponse("<h1>Successfully deleted uav from DB.</h1>")


@csrf_exempt
def manage_hubs(request):

    # Создание в БД хабов для кейса Якутска в режиме пресета
    if request.method == "POST":
        database.manual_hubs_creation()
        return HttpResponse("Successfully added hubs data to DB.")

    # Удаление всех данных хабов из БД
    elif request.method == "DELETE":
        HUB.objects.all().delete()
        return HttpResponse("Successfully erased all hub data.")


def manage_single_hub(request, hub_id):
    # Отправка данных по конкретному хабу
    if request.method == "GET":
        hub = HUB.objects.get(hub_id=hub_id)
        hub_data = {'id': int(hub.hub_id),
                    'type': hub.type,
                    'workload': hub.workload,
                    'latitude': hub.latitude,
                    'longitude': hub.longitude}
        return HttpResponse(json.dumps(hub_data), content_type="application/json")
