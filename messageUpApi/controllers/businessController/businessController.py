# api/controllers/businessController/businessController.py
from .businessTasks.businessTasks import *

def business_controller(method, request, slug,user=None):
    if method == "GET":
        return get_business_task(slug,user)
    if method == "POST":
        return create_business_task(request.user, request.data)
    if method == "PUT":
        return update_business_task(request.user, request.data)
    if method == "DELETE":
        return delete_business_task(request.user)

def getBusinessData(user=None):
    try:
        business = None
        data = []
        if user:
            business = Business.objects.get(user=user)
            data = get_business_data(business)
        else:
            business = Business.objects.all()
            data = [get_business_data(b) for b in business]
        return True, data, 200
    except Business.DoesNotExist:
        return False, {"error": "not_found"}, 404