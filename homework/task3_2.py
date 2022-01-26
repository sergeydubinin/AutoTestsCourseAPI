# Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_cookie
# Этот метод возвращает какую-то cookie с каким-то значением. Необходимо с помощью функции print() понять что за cookie
# и с каким значением, и зафиксировать это поведение с помощью assert

import requests


class TestHomeWork:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        response_cookie = dict(response.cookies)

        assert response.status_code == 200, "Wrong response code"
        assert "HomeWork" in response_cookie, "There is no cookie 'HomeWork' in the response"
        assert response_cookie["HomeWork"] == "hw_value", "Actual cookie in the response is not correct"
