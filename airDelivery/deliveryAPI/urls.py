from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('orders', views.manage_orders),
    path('drones/<int:drone_id>/', views.manage_drone),
    path('orders/<int:order_id>/', views.update_order),
    path('drones', views.get_drone_locations)
]
