from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Изменение данных пользователя")
class TestUserEdit(BaseCase):
    @allure.title("Изменение имени только что созданного пользовтаеля")
    @allure.description("Данный тест проверяет успешность изменения имени только что зарегистрированного пользователя")
    def test_edit_just_created_user(self):
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

        # EDIT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    @allure.title("Изменение имени пользователя будучи неавторизованным")
    @allure.description("Данный тест проверяет невозможность изменения имени пользователя будучи неавторизованным")
    def test_edit_user_without_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, 'id')

        # EDIT
        new_name = "Changed name"
        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_text(response2, "Auth token not supplied")

    @allure.title("Изменение имени другого пользователя")
    @allure.description("Данный тест проверяет невозможность изменения имени пользователя с другим ID")
    def test_edit_being_authorized_as_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, 'id')

        # LOGIN AS OTHER USER
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_text(response3, "Please, do not edit test users with ID 1, 2, 3, 4 or 5.")

    @allure.title("Изменение email пользователя на некорректный")
    @allure.description("Данный тест проверяет невозможность изменения email пользователя на некорректный")
    def test_edit_to_invalid_email(self):
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

        # EDIT
        new_email = "newemail.ru"
        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_text(response3, "Invalid email format")

    @allure.title("Изменение имени пользователя на некорректное")
    @allure.description("Данный тест проверяет невозможность изменения имени пользователя на некорректное")
    def test_edit_to_invalid_first_name(self):
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

        # EDIT
        new_name = "a"
        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName",
                                             "Wrong error message")
