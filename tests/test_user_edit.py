import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    def test_edit_user_without_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, 'id')

        # EDIT
        new_name = "Changed name"
        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", data={"firstName": new_name})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_text(response2, "Auth token not supplied")

    def test_edit_being_authorized_as_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        user_id = self.get_json_value(response1, 'id')

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN AS OTHER USER
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_text(response3, "Please, do not edit test users with ID 1, 2, 3, 4 or 5.")

    def test_edit_to_invalid_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = "newemail.ru"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, data={"email": new_email})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_text(response3, "Invalid email format")

    def test_edit_to_invalid_first_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "a"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName",
                                             "Wrong error message")
