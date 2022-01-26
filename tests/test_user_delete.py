from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_hardcoded_user_id_2(self):
        # LOGIN
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete("/user/2", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_text(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

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

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response4, 404)
        Assertions.assert_response_text(response4, "User not found")

    def test_delete_being_authorized_as_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        user_id = self.get_json_value(response1, 'id')

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN AS OTHER USER
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_text(response3, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")
