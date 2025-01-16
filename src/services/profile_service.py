import requests

from src.services.base_service import BaseService, login_required


class ProfileService(BaseService):

    @login_required
    def get_profile(self):
        response = requests.get(self.BASE_URL + "/profiles/", headers=self.get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"failed: {response.json()}")

    @login_required
    def update_profile(self, data):
        # Prepare the files for the API request (if an image is provided)
        files = {}
        if "image" in data and data["image"]:
            files["image"] = ("profile_image.jpg", data["image"], "image/jpeg")

        # Remove the image from the data dictionary (if it exists)
        data.pop("image", None)

        # Send the request to the Django REST API
        response = requests.patch(
            self.BASE_URL + "/profiles/",
            headers=self.get_headers(),
            data=data,  # Send form data
            files=files if files else None,  # Send files (if any)
        )

        # Check the response status
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"failed: {response.json()}")
