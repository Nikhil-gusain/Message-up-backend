# api/controllers/metaController/metaController.py
from .metaTasks.metaTasks import (
    get_business_categories_task,
    get_product_categories_task,
    get_user_types_task,
)

def business_category_controller(request):
    return get_business_categories_task(request.query_params)

def product_category_controller(request):
    return get_product_categories_task(request.query_params)

def user_type_controller(request):
    return get_user_types_task(request.query_params)
