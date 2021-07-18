from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.manage_orders),
    path('drones/<int:drone_id>', views.manage_single_uav),
    path('orders/<int:order_id>', views.manage_single_order),
    path('drones', views.manage_drone_fleet),
    path('hubs', views.manage_hubs),
    path('hubs/<int:hub_id>', views.manage_single_hub),
    path('drones/<int:drone_id>/orders', views.manage_orders_carried_by_uav),
    path('orders/<int:order_id>/track', views.manage_order_track),
    path('drones/<int:drone_id>/track', views.manage_uav_track),
    path('acceleration', views.apply_acceleration),
    path('statistics', views.get_statistics),
    path('statistics/new', views.create_statistics),
    path('orders/<int:order_id>/finish', views.order_finishing)
]
