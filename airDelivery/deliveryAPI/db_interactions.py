from .models import ORDER, BPLA, HUB
import datetime


def create_order(order_params):
    track_string = str(order_params['track'])
    new_order = ORDER(weight=order_params['weight'],
                      cur_departure=HUB.objects.get(hub_id=(int(order_params['first_hub']))),
                      cur_destination=HUB.objects.get(hub_id=(int(order_params['track']["Product_path"][1]["HubID"]))),
                      bpla=None,
                      track=track_string,
                      start_time=datetime.datetime.now())
    new_order.save()
    new_order.order_id = new_order.id
    new_order.save()
    return new_order


def create_uav(uav_params):
    new_uav = BPLA(board_number=str(uav_params['board_number']),
                   type=uav_params['type'],
                   capacity=uav_params['capacity'],
                   speed=uav_params['speed'],
                   latitude=uav_params['latitude'],
                   longitude=uav_params['longitude'],
                   azimuth=uav_params['azimuth'],
                   departure_hub=uav_params['departure_hub'],
                   destination_hub=uav_params['destination_hub'],
                   lat_delta=uav_params['lat_delta'],
                   long_delta=uav_params['long_delta'])
    new_uav.save()


def manual_hubs_creation():
    new_hub_data = {"type": [], "workload": [],  "latitude": [], "longitude": [], "hub_id": []}
    f = open('deliveryAPI/validated_hubs.txt')
    for line in f:
        data = line.split()
        new_hub_data["type"].append(int(data[0]))
        new_hub_data["workload"].append(1)
        new_hub_data["latitude"].append(float(data[2]))
        new_hub_data["longitude"].append(float(data[1]))
        new_hub_data["hub_id"].append(int(data[3]))
    for i in range(len(new_hub_data['type'])):
        new_hub = HUB(type=new_hub_data['type'][i],
                      workload=new_hub_data['workload'][0],
                      latitude=new_hub_data['latitude'][i],
                      longitude=new_hub_data['longitude'][i],
                      hub_id=new_hub_data['hub_id'][i])
        new_hub.save()
        print(new_hub.hub_id)
