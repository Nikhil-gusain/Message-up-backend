# api/controllers/statusController/statusTasks/statusTasks.py
from messageUpApi.models import Status, Business

def get_status_task(slug=None, user=None):
    qs=[]
    if slug is None:
        qs = Status.objects.filter(business__user=user)
    else:
        qs = Status.objects.filter(business__slug=slug)
    return True, [{"id": s.id, "image": s.image.url} for s in qs], 200

def create_status_task(user, data):
    try:
        biz = Business.objects.get(user=user)
        obj = Status.objects.create(business=biz, image=data["image"])
        return True, {"id": obj.id}, 201
    except Exception:
        return False, {"error": "invalid"}, 400

def delete_status_task(user, data):
    try:
        Status.objects.get(id=data["id"], business__user=user).delete()
        return True, None, 204
    except Status.DoesNotExist:
        return False, {"error": "not_found"}, 404
