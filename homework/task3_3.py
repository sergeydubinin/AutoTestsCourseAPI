# Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_header
# Этот метод возвращает headers с каким-то значением. Необходимо с помощью функции print() понять что за headers и с
# каким значением, и зафиксировать это поведение с помощью assert

import requests


class TestHomeWork:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        assert response.status_code == 200, "Wrong response code"
        assert "x-secret-homework-header" in response.headers, "There is no header 'x-secret-homework-header' in the " \
                                                               "response"
        assert response.headers["x-secret-homework-header"] == "Some secret value", "Actual cookie in the response " \
                                                                                    "is not correct"
