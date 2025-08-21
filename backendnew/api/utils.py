import secrets
from django.core.cache import cache

def generate_token(user_id):
    """
    Generate a secure token and store it in cache with 1-hour validity.
    """
    token = secrets.token_urlsafe(32)
    cache.set(token, user_id, timeout=3600)  # valid for 1 hour
    return token

def verify_token(token):
    """
    Verify the token and return user_id if valid, else None.
    """
    return cache.get(token)
