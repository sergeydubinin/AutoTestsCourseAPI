# У нас есть вот такой URL: https://playground.learnqa.ru/ajax/api/compare_query_type
# Запрашивать его можно четырьмя разными HTTP-методами: POST, GET, PUT, DELETE

# При этом в запросе должен быть параметр method. Он должен содержать указание метода, с помощью которого вы делаете
# запрос. Например, если вы делаете GET-запрос, параметр method должен равняться строке ‘GET’. Если POST-запросом - то
# параметр method должен равняться ‘POST’. И так далее.

# Написать скрипт, который делает следующее:
# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
response1 = requests.get(url)
print(response1.text)
response2 = requests.patch(url, data={"method": "PATCH"})
print(response2.text)
response3 = requests.get(url, params={"method": "GET"})
print(response3.text)


def error_print():
    print(f"Запрос с ошибкой! Тип запроса: {method}, значение параметра: {param['method']}. Ответ: {response.text}."
          f" Статус код: {response.status_code}")


def check_response():
    if method != param["method"] and response.text == '{"success":"!"}':
        error_print()
    elif method == param["method"] and response.text != '{"success":"!"}':
        error_print()


methods = ["GET", "POST", "PUT", "DELETE"]
params = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]
for method in methods:
    for param in params:
        if method == "GET":
            response = requests.request(method, url, params=param)
            check_response()
        else:
            response = requests.request(method, url, data=param)
            check_response()
