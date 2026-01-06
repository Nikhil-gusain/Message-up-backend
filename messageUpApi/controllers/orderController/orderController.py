# api/controllers/orderController/orderController.py
from .orderTasks.orderTasks import *

def user_order_controller(method, request):
    if method == "GET":
        return get_user_orders_task(request.user)
    if method == "POST":
        return create_order_task(request.user, request.data)

def business_order_controller(method, request):
    if method == "GET":
        return get_business_orders_task(request.user)
    if method == "PUT":
        return update_order_status_task(request.data)
