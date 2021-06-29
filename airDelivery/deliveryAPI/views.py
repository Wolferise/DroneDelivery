from django.http import HttpResponse
import json
from .models import ORDER, BPLA, HUB
import datetime
import math
from .requests import calculate_order_route, send_order_to_first_hub
from django.views.decorators.csrf import csrf_exempt


def index(request):
    if request.method == "GET":  # Обработка запроса на создание нового заказа
        new_order_data = request.GET
        print(new_order_data)
        # Запрос на построение маршрута
        math_module_answer = json.loads(calculate_order_route(new_order_data['weight'], new_order_data['first_hub'],
                                                   new_order_data['last_hub']).content)
        track = str(math_module_answer)
        # Запись в БД
        drone_id = add_drone(new_order_data['first_hub'], math_module_answer["Product_path"][1]["HubID"])
        new_order = ORDER(weight=new_order_data['weight'],
                          cur_departure=new_order_data['first_hub'],
                          cur_destination=math_module_answer["Product_path"][1]["HubID"],
                          bpla=drone_id,
                          track=track,
                          start_time=datetime.datetime.now())
        new_order.save()
        # Передача заказа в Хаб
        send_order_to_first_hub(new_order_data.first_hub, new_order.id)
        add_drone()
        return HttpResponse("<h1>Success</h1>")
    else:
        return HttpResponse("<h1>Inappropriate request type.</h1>")


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
        order.bpla = order_data['bpla']
        order.cur_departure = order_data['dep_hub_id']
        if order_data['dest_hub_id'] is not None:
            order.cur_destination = order_data['dest_hub_id']
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
        #drones = BPLA.objects.filter(latitude__gte=screen_data.less_latitude
        #                             ).filter(latitude__lte=screen_data.more_latitude
        #                             ).filter(longitude__gte=screen_data.less_longitude
        #                             ).filter(longitude__lte=screen_data.more_longitude)
        drones = BPLA.objects.all()
        drone_data = dict()
        for drone in drones:
            drone_data.update({drone.id: [drone.latitude, drone.longitude, drone.speed, drone.azimuth]})
        drone_data = json.dumps(drone_data)
        return HttpResponse(drone_data, content_type="application/json")


@csrf_exempt
def manage_graph(request):
    if request.method == "POST":
        new_hub_data = request.POST
        print(new_hub_data)
        new_hub = HUB(type=new_hub_data['type'],
                      workload=new_hub_data['workload'],
                      latitude=new_hub_data['latitude'],
                      longitude=new_hub_data['longitude'])
        new_hub.save()
        return HttpResponse("<h1>Success</h1>")
    elif request.method == "DELETE":
        hub_data = request.DELETE
        HUB.objects.filter(id=hub_data.hub_id).delete()
        return HttpResponse("<h1>Success</h1>")
    elif request.method == "GET":
        new_hub_data = request.GET
        print(new_hub_data)
        new_hub = HUB(type=new_hub_data['type'],
                      workload=new_hub_data['workload'],
                      latitude=new_hub_data['latitude'],
                      longitude=new_hub_data['longitude'])
        new_hub.save()
        return HttpResponse("<h1>Success</h1>")
        #hub_data = request.GET
        #hub = HUB.objects.filter(id=hub_data['hub_id'])
        #hub_data = {'type': hub.type, 'workload': hub.workload, 'latitude': hub.latitude, 'longitude': hub.longitude}
        #response = json.dumps(hub_data)
        #return HttpResponse(response, content_type="application/json")

def add_drone(cur_hub, next_hub):
    cur_hub_data = HUB.objects.filter(id=cur_hub)
    dest_hub_data = HUB.objects.filter(id=next_hub)
    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795

    # координаты двух точек
    llat1 = float(cur_hub_data.latitude)
    llong1 = float(cur_hub_data.longitude)

    llat2 = float(dest_hub_data.latitude)
    llong2 = float(dest_hub_data.longitude)

    # в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисление начального азимута
    x = (cl1 * sl2) - (sl1 * cl2 * cdelta)
    y = sdelta * cl2
    z = math.degrees(math.atan(-y / x))

    if x < 0:
        z = z + 180.

    z2 = (z + 180.) % 360. - 180.
    z2 = - math.radians(z2)
    anglerad2 = z2 - ((2 * math.pi) * math.floor((z2 / (2 * math.pi))))
    angledeg = (anglerad2 * 180.) / math.pi

    new_drone = BPLA(board_number='one',
                     type='small',
                     capacity=500,
                     speed=20.0,
                     latitude=cur_hub_data.latitude,
                     longitude=cur_hub_data.longitude,
                     azimuth=angledeg)
    new_drone.save()
    return new_drone.id