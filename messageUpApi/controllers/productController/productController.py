# api/controllers/productController/productController.py
from .productTasks.productTasks import *

def product_controller(method, request, slug):
    if method == "GET":
        return get_product_task(slug, request.query_params)

def business_product_controller(method, request, slug,user=None):
    if method == "GET":
        return get_business_products_task(user=user, slug=slug)
    if method == "POST":
        return create_product_task(request.user, request.data)
    if method == "PUT":
        return update_product_task(request.user, slug, request.data)
    if method == "DELETE":
        return delete_product_task(request.user, slug)

def product_by_category_controller(category_id, request):
    return get_products_by_category_task(category_id, request.query_params)

def business_by_category_controller(category_id, request):
    return get_business_by_category_task(category_id, request.query_params)
