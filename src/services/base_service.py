from functools import wraps

import requests

from src import config
from src.database import redis_store


def login_required(func):
    """Decorator to handle 401 errors automatically."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.handle_401()
        return func(self, *args, **kwargs)  # Proceed to the actual function if authorized

    return wrapper


class BaseService:
    BASE_URL = config.API_BASE_URL + "/api/v1"

    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.access_token, self.refresh_token = redis_store.get_token(telegram_id)

    def get_headers(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        return headers

    def check_access_token(self):
        """Checks if the access token is valid. If not, attempt to refresh it."""
        if not self.access_token:
            return False

        # Example: making a request to validate the token (replace with your actual validation logic)
        response = requests.post(f"{self.BASE_URL}/auth/token/verify/", json={"token": self.access_token})

        if response.status_code == 401:  # Token is invalid or expired
            return False

        return True

    def refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        response = requests.post(f"{self.BASE_URL}/auth/token/refresh/", json={"refresh_token": self.refresh_token})

        if response.status_code == 200:
            new_tokens = response.json()  # Assuming the new tokens are returned in the response
            self.access_token = new_tokens.get("access_token")
            self.refresh_token = new_tokens.get("refresh_token")
            redis_store.set_token(self.telegram_id, self.access_token, self.refresh_token)
            return True

        return False

    def get_token_pair(self):
        """Get a pair of access token and refresh token."""
        data = {
            "telegram_profile": {
                "telegram_id": self.telegram_id,
            }
        }
        response = requests.post(f"{self.BASE_URL}/auth/login/token/", json=data)
        tokens = response.json()
        redis_store.set_token(self.telegram_id, tokens["access"], tokens["refresh"])

    def handle_401(self):
        """Handle a 401 Unauthorized error by checking authentication and refreshing the token."""
        if not self.check_access_token():
            if not self.refresh_access_token():
                self.get_token_pair()
