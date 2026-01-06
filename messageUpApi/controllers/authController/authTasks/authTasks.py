from messageUpApi.models import User
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken

def verify_google_token(id_token_str):
    try:
        info = id_token.verify_oauth2_token(
            id_token_str,
            requests.Request(),
            settings.GOOGLE_OAUTH2_CLIENT_ID
        )
        if info.get("email_verified"):
            return True, info
        return False, {"error": "email_not_verified"}
    except Exception:
        return False, {"error": "invalid_token"}

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

def google_auth_task(id_token_str):
    ok, result = verify_google_token(id_token_str)
    if not ok:
        return False, result

    email = result.get("email")
    name = result.get("name", "")
    sub = result.get("sub")

    user, created = User.objects.get_or_create(email=email, defaults={
        "username": email.split("@")[0],
    })

    tokens = get_tokens_for_user(user)

    return True, {
        "user": {"id": user.id, "email": user.email, "username": user.username},
        "tokens": tokens,
    }
