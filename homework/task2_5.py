# Сегодня к нам пришел наш коллега и сказал, что забыл свой пароль от важного сервиса. Он просит нас помочь ему написать
# программу, которая подберет его пароль.
# Условие следующее. Есть метод: https://playground.learnqa.ru/ajax/api/get_secret_password_homework
# Его необходимо вызывать POST-запросом с двумя параметрами: login и password
# Если вызвать метод без поля login или указать несуществующий login, метод вернет 500
# Если login указан и существует, метод вернет нам авторизационную cookie с названием auth_cookie и каким-то значением.
# У метода существует защита от перебора. Если верно указано поле login, но передан неправильный password,
# то авторизационная cookie все равно вернется. НО с "неправильным" значением, которое на самом деле не позволит
# создавать авторизованные запросы. Только если и login, и password указаны верно, вернется cookie с "правильным"
# значением. Таким образом используя только метод get_secret_password_homework невозможно узнать, передали ли мы верный
# пароль или нет. По этой причине нам потребуется второй метод, который проверяет правильность нашей авторизованной
# cookie: https://playground.learnqa.ru/ajax/api/check_auth_cookie
# Если вызвать его без cookie с именем auth_cookie или с cookie, у которой выставлено "неправильное" значение, метод
# вернет фразу "You are NOT authorized". Если значение cookie “правильное”, метод вернет: “You are authorized”
# Коллега говорит, что точно помнит свой login - это значение super_admin. А вот пароль забыл, но точно помнит, что
# выбрал его из списка самых популярных паролей на Википедии.
# Ссылка: https://en.wikipedia.org/wiki/List_of_the_most_common_passwords
# Искать его нужно среди списка Top 25 most common passwords by year according to SplashData
# Итак, наша задача - написать скрипт и указать в нем login нашего коллеги и все пароли из Википедии в виде списка.
# Программа должна делать следующее:
# 1. Брать очередной пароль и вместе с логином коллеги вызывать первый метод get_secret_password_homework. В ответ метод
# будет возвращать авторизационную cookie с именем auth_cookie и каким-то значением.
# 2. Далее эту cookie мы должна передать во второй метод check_auth_cookie. Если в ответ вернулась фраза "You are NOT
# authorized", значит пароль неправильный. В этом случае берем следующий пароль и все заново. Если же вернулась другая
# фраза - нужно, чтобы программа вывела верный пароль и эту фразу.

import requests

password = ['admin', 'football', 'starwars', 1234567, 111111, 696969, 'baseball', 'ninja', 'azerty', 'welcome',
            'qazwsx', 'qwertyuiop', 123456789, 'qwerty', 'solo', 'freedom', 'shadow', '1q2w3e4r', '000000', 'whatever',
            'password', '1qaz2wsx', 'mustang', 'flower', 555555, 'jesus', 'michael', 666666, 'lovely', 'charlie',
            '654321', '123qwe', 'adobe123[a]', 'monkey', 'photoshop[a]', 'superman', 121212, 12345, 888888, 'hottie',
            'passw0rd', 'batman', 'trustno1', 'bailey', 123456, 'letmein', 'password1', 'hello', 'aa123456', 12345678,
            1234, 1234567890, 'master', 'access', 'iloveyou', 'zaq1zaq1', 'abc123', 'donald', 'qwerty123', 654321,
            7777777, 'princess', 123123, '!@#$%^&*', 'sunshine', 'login', 'loveme', 'dragon', 'ashley', 'Football']

for i in range(len(password)):
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                              data={"login": "super_admin", "password": password[i]})
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie",
                              cookies=dict(response1.cookies))
    if response2.text != "You are NOT authorized":
        print(f"{response2.text}. Password: {password[i]}")
        break
