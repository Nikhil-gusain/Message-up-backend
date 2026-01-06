# api/controllers/statusController/statusController.py
from .statusTasks.statusTasks import *

def status_controller(method, request, slug=None):
    if method == "GET":
        return get_status_task(slug=slug,user = request.user if request.user.is_authenticated else None)
    if method == "POST":
        return create_status_task(request.user, request.data)
    if method == "DELETE":
        return delete_status_task(request.user, request.data)
