from .models import ORDER, BPLA, HUB
import datetime


def create_order(order_params, order_track):
    track_string = str(order_track)
    new_order = ORDER(weight=order_params['weight'],
                      cur_departure=HUB.objects.get(hub_id=(int(order_params['first_hub']))),
                      cur_destination=HUB.objects.get(hub_id=(int(order_track["Product_path"][1]["HubID"]))),
                      bpla=None,
                      track=track_string,
                      start_time=datetime.datetime.now())
    new_order.save()
    return new_order


def create_uav(uav_params):
    new_uav = BPLA(board_number=str(uav_params['board_number']),
                   type=uav_params['type'],
                   capacity=uav_params['capacity'],
                   speed=uav_params['speed'],
                   latitude=uav_params['latitude'],
                   longitude=uav_params['longitude'],
                   azimuth=uav_params['azimuth'])
    new_uav.save()


def manual_hubs_creation():
    new_hub_data = {"type": [2, 1, 0, 0, 0,
                             1, 0, 0, 0, 0,
                             1, 0, 0, 0, 0],
                    "workload": [1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1],
                    "latitude": [62.027116, 62.192133, 62.188151, 62.221784, 62.257617,
                                 62.530460, 62.585172, 62.627082, 62.665896, 62.680782,
                                 61.536701, 61.614186, 61.484245, 61.535072, 61.486290],
                    "longitude": [129.731981, 130.713196, 130.673728, 130.684686, 130.720085,
                                  129.762779, 129.770292, 129.714927, 129.704122, 129.911464,
                                  129.182589, 129.228230, 129.148212, 129.411281, 129.320305],
                    "hub_id": [0, 1, 2, 3, 4,
                               5, 6, 7, 8, 9,
                               10, 11, 12, 13, 14]}
    for i in range(len(new_hub_data['type'])):
        new_hub = HUB(type=new_hub_data['type'][i],
                      workload=new_hub_data['workload'][i],
                      latitude=new_hub_data['latitude'][i],
                      longitude=new_hub_data['longitude'][i],
                      hub_id=new_hub_data['hub_id'][i])
        new_hub.save()
