from rest_framework import routers
from django.urls import path
from . import views
urlpatterns = [
    path('add_dish/<int:pk>/',views.increase_dish,name='add_dish'),
    path('decrease_dish/<int:pk>/',views.decrease_dish,name='decrease_dish'),
    path('my_cart/<int:pk>/',views.my_cart,name='my_cart'),
    path('my_orders/<int:pk>/',views.my_orders,name='my_orders'),
    path('order_by_id/<int:pk>/',views.order_by_id,name='order_by_id'),
    path('order_by_id_edit/<int:pk>/',views.order_by_id_edit,name='order_by_id_edit'),
    path('all_orders/',views.all_orders,name='all_orders'),
    path('add_coupon/<int:pk>/',views.add_coupon,name='add_coupon'),
    path('add_address/<int:pk>/',views.add_address,name='add_address'),
    path('checkout/<int:pk>/',views.checkout,name='checkout'),
    ]