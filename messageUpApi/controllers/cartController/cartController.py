# api/controllers/cartController/cartController.py
from .cartTasks.cartTasks import *

def cart_controller(method, request, item_id):
    if method == "GET":
        return get_cart_task(request.user)
    if method == "PUT":
        return add_cart_task(request.user, request.data)
    if method == "DELETE":
        return delete_cart_task(request.user, item_id)
