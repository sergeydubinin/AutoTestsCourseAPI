# API-метод находится по следующему URL: https://playground.learnqa.ru/ajax/api/longtime_job
# Если мы вызываем его БЕЗ GET-параметра token, метод заводит новую задачу, а в ответ выдает нам JSON со следующими
# полями:
# * seconds - количество секунд, через сколько задача будет выполнена
# * token - тот самый токен, по которому можно получить результат выполнения нашей задачи

# Если же вызвать метод, УКАЗАВ GET-параметром token, то мы получим следующий JSON:
# * error - будет только в случае, если передать token, для которого не создавалась задача. В этом случае в ответе будет
# следующая надпись - No job linked to this token
# * status - если задача еще не готова, будет надпись Job is NOT ready, если же готова - будет надпись Job is ready
# * result - будет только в случае, если задача готова, это поле будет содержать результат

# Задача - написать скрипт, который делал бы следующее:
# 1) создавал задачу
# 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
# 3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
# 4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля
# result

import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"


def check_response(response):
    if response.json()["status"] == "Job is ready" and "result" in response.json():
        return True
    else:
        return False


def result_print(response):
    if check_response(response):
        print(f"Статус: {response.json()['status']}. Результат: {response.json()['result']}")
    else:
        print("Error!")


response1 = requests.get(url)
response2 = requests.get(url, params={"token": response1.json()["token"]})
if response2.json()["status"] == "Job is NOT ready":
    time.sleep(response1.json()["seconds"])
    response3 = requests.get(url, params={"token": response1.json()["token"]})
    result_print(response3)
else:
    result_print(response2)
