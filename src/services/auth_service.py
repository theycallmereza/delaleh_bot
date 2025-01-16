import requests

from src.config import API_BASE_URL


class AuthService:
    BASE_URL = API_BASE_URL

    def __init__(self, api_key, mobile_number, telegram_id, username, first_name, last_name, language_code):
        self.api_key = api_key
        self.mobile_number = mobile_number
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code

    def login(self):
        """Authenticate the user and get JWT tokens."""
        url = f"{self.BASE_URL}/api/v1/auth/login/token/"
        payload = {
            "api_key": self.api_key,
            "mobile_number": self.mobile_number,
            "username": self.username,
            "telegram_profile": {
                "telegram_id": self.telegram_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "language_code": self.language_code,
            },
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return response.json()  # Returns JWT tokens
        else:
            raise Exception(f"Authentication failed: {response.json()}")
