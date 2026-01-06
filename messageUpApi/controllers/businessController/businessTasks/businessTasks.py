# api/controllers/businessController/businessTasks/businessTasks.py
from messageUpApi.models import Business, BusinessCategory

def get_business_data(business:Business):
    try:
        data = {
            "id": business.id,
            "name": business.name,
            "slug": business.slug,
            "description": business.description,
            "address": business.address,
            "phone": business.phone,
            "category": {
                "id": business.category.id,
                "label": business.category.label,
                "value": business.category.value
            },
            "profile": business.profile.url if business.profile else '',
            "user": {
                "id": business.user.id,
                "username": business.user.username,}
        }
        return data
    except Business.DoesNotExist:
        return {
            "error": "not_found"
        }

def get_business_task(slug=None,user=None):
    try:
        obj=None
        if user:
            obj = Business.objects.get(user=user)
        else:
            obj = Business.objects.get(slug=slug)
        data = get_business_data(obj)
        return True,data, 200
    except Business.DoesNotExist:
        return False, {"error": "not_found"}, 404

def create_business_task(user, data):
    try:
        if hasattr(data, 'dict'):
            data = data.dict()
        else:
            data = data.copy()
            
        cat_id = data.pop("category")
        cat = BusinessCategory.objects.get(id=cat_id)
        obj = Business.objects.create(user=user, category=cat, **data)
        status,returnData,code = get_business_task(obj.slug)
        return status, returnData, code
    except Exception as e:
        print(f"DEBUG EXCEPTION in create_business_task: {e}")
        return False, {"error": "invalid"}, 400

def update_business_task(user, data):
    try:
        obj = Business.objects.get(user=user)
        if "category" in data:
            cat_id = data.pop("category")
            cat = BusinessCategory.objects.get(id=cat_id)
            setattr(obj, "category", cat)
        for k, v in data.items():
            setattr(obj, k, v)
        obj.save()
        status,returnData,code = get_business_task(obj.slug)
        return status, returnData, code
    except Business.DoesNotExist:
        return False, {"error": "not_found"}, 404

def delete_business_task(user):
    try:
        Business.objects.get(user=user).delete()
        return True, None, 204
    except Business.DoesNotExist:
        return False, {"error": "not_found"}, 404
