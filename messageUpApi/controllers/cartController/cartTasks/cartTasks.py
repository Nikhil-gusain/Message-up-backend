# api/controllers/cartController/cartTasks/cartTasks.py
from messageUpApi.models import Cart, CartItem, Product

def get_cart_task(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    data = []
    for item in cart.items.all():
        p = item.product
        data.append({
            "name": p.name,
            "slug": p.slug,
            "price": p.price,
            "quantity": item.quantity,
        })
    return True, {"id": cart.id, "product": data}, 200

def add_cart_task(user, data):
    try:
        product = Product.objects.get(slug=data["product"])
        item, created = CartItem.objects.get_or_create(
            product=product, 
            defaults={"quantity": data["quantity"]}
        )
        if not created:
            item.quantity = data["quantity"]
            item.save()
        cart, _ = Cart.objects.get_or_create(user=user)
        cart.items.add(item)
        return True, None, 200
    except Product.DoesNotExist:
        return False, {"error": "product_not_found"}, 404

def delete_cart_task(user, item_id):
    cart = Cart.objects.get(user=user)
    if item_id:
        cart.items.remove(item_id)
    else:
        cart.items.clear()
    return True, None, 204
