# api/controllers/orderController/orderTasks/orderTasks.py
from messageUpApi.models import Order, Cart, CartItem, Business,Product
from messageUpApi.controllers.cartController.cartTasks.cartTasks import *
from django.db import transaction

def get_order_data(order:Order):
    products:list[Product] = []
    for item in order.items.all():
        p:Product = item.product
        products.append({
            "name": p.name,
            "slug": p.slug,
            "price": p.price,
            "quantity": item.quantity
        })
    return {
        "id": order.id,
        "price": order.price,
        "status": order.status,
        "business": order.business.name,
        "user": order.user.username,
        "created_at": order.created_at,
        "products": products
    }

def get_user_orders_task(user):
    orders = Order.objects.filter(user=user).order_by("-created_at")
    data = []
    for o in orders:
        data.append(get_order_data(o))
    return True, data, 200


def get_business_orders_task(user):
    try:
        business = Business.objects.get(user=user)
    except Business.DoesNotExist:
        return False, {"error": "business_not_found"}, 404

    orders = Order.objects.filter(business=business).order_by("-created_at")
    data = []
    for o in orders:
        data.append(get_order_data(o))
    return True, data, 200


@transaction.atomic
def create_order_task(user, data):
    try:
        cart = Cart.objects.get(user=user)
        if not cart.items.exists():
            return False, {"error": "cart_empty"}, 400

        total_price = 0
        business = None
        items = []

        for item in cart.items.select_related("product"):
            total_price += item.product.price * item.quantity
            business = item.product.business
            items.append(item)

        order = Order.objects.create(
            user=user,
            business=business,
            price=total_price,
            status="created",
        )
        order.items.set(items)

        cart.items.clear()
        return True, get_order_data(order), 201
    except Cart.DoesNotExist:
        return False, {"error": "cart_not_found"}, 404


def update_order_status_task(data):
    try:
        order = Order.objects.get(id=data["order_id"])
        order.status = data["status"]
        order.save()
        return True, get_order_data(order), 200
    except Order.DoesNotExist:
        return False, {"error": "order_not_found"}, 404
