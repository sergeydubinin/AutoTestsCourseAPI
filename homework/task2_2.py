# Необходимо написать скрипт, который создает GET-запрос на метод: https://playground.learnqa.ru/api/long_redirect
# С помощью конструкции response.history необходимо узнать, сколько редиректов происходит от изначальной точки
# назначения до итоговой. И какой URL итоговый.

import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print("Количество редиректов:", len(response.history))
print("Итоговый URL:", response.url)
