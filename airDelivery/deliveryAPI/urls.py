from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.manage_orders),
    path('drones/<int:drone_id>/', views.manage_single_uav),
    path('orders/<int:order_id>/', views.manage_single_order),
    path('drones', views.manage_drone_fleet),
    path('hubs', views.manage_hubs)
]
