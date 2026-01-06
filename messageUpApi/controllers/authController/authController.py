from .authTasks.authTasks import google_auth_task

def google_auth_controller(data):
    try:
        id_token = data.get("id_token")
        ok, payload = google_auth_task(id_token)
        if not ok:
            return False, payload, 400

        return True, payload, 200
    except Exception as e:
        return False, {"error":"internal_error"}, 500
