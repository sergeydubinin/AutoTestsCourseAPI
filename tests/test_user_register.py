from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

urn = "/user"


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(urn, data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post(urn, data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, f"Users with email '{email}' already exists")

    def test_create_user_invalid_email(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post(urn, data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "Invalid email format")

    data_empty_field = [
        ({"password": "", "username": "learnqa", "firstName": "learnqa", "lastName": "learnqa",
          "email": "vinkotov@example.com"}),
        ({"password": "123", "username": "", "firstName": "learnqa", "lastName": "learnqa",
          "email": "vinkotov@example.com"}),
        ({"password": "123", "username": "learnqa", "firstName": "", "lastName": "learnqa",
          "email": "vinkotov@example.com"}),
        ({"password": "123", "username": "learnqa", "firstName": "learnqa", "lastName": "",
          "email": "vinkotov@example.com"}),
        ({"password": "123", "username": "learnqa", "firstName": "learnqa", "lastName": "learnqa", "email": ""})
    ]

    @pytest.mark.parametrize("data", data_empty_field)
    def test_create_user_with_empty_field(self, data):
        response = MyRequests.post(urn, data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, f"The value of '{list(data.keys())[list(data.values()).index('')]}' "
                                                  f"field is too short")

    def test_create_user_with_short_first_name(self):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "l",
            "lastName": "learnqa",
            "email": "vinkotov@example.com"
        }

        response = MyRequests.post(urn, data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "The value of 'firstName' field is too short")

    def test_create_user_with_long_first_name(self):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": f"{'l' * 251}",
            "lastName": "learnqa",
            "email": "vinkotov@example.com"
        }

        response = MyRequests.post(urn, data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "The value of 'firstName' field is too long")
