import vk_api
import random
import time
import sqlite3

conn = sqlite3.connect('KARO2.db')
cursor = conn.cursor()

conn1 = sqlite3.connect('mirage4.db')
cursor1 = conn1.cursor()

token = ""

vk = vk_api.VkApi(token=token)

vk._auth_token()

remember_cinema_num = ''

main_id = 0

helloes = ["привет", "дороу", "здравствуйте", "прием", "хелло", "салам"]

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            check = body.lower()
            if body.lower() in helloes:
                hello = body.lower()
                hello = hello[0].upper() + hello[1:]
                vk.method("messages.send",
                          {"peer_id": id,
                           "message": f"{hello}! \n Напишите 'посмотреть кинотеатры' и номер сети из списка. \n Пример: 'посмотреть кинотеатры 228' \n Доступные сети кинотеатров: \n 1) Сеть кинотеатров КАРО \n 2) Сеть кинотеатров Мираж Синема", "random_id": random.randint(1, 2147483647)})

            elif body.lower()[:-2] == "посмотреть кинотеатры" and body.lower()[-1] == '1':
                main_id = 1
                cinemas_lst = list(cursor.execute("select distinct name_theather from cinemas"))
                cinemas_ids = list(cursor.execute("select distinct id_cinema FROM cinemas"))
                cinemas_lst1 = []
                cinemas_ids1 = []
                for i in cinemas_lst:
                    cinemas_lst1.append(i[0])
                for i in cinemas_ids:
                    cinemas_ids1.append(str(i[0]))
                cinemas_end = []
                for i, e in enumerate(cinemas_lst1, 1):
                    cinemas_end.append(f'{i}) {e}')
                c = ''
                for i in cinemas_end:
                    c += i + '\n'
                vk.method("messages.send", {"peer_id": id,
                                            "message": f"Напиши 'кинотеатр' и его номер в списке для продложения. \n Пример: кинотеатр 228 \n Список кинотеатров сети КАРО: \n {c} ",
                                            "random_id": random.randint(1, 2147483647)})

            elif str(body.lower()).count(' ') == 1 and (str(body.lower()).split(' ')[1] in cinemas_ids1) and (
                    str(body.lower()).split(' ')[0] == 'кинотеатр') and main_id == 1:
                remember_cinema_num = str(body.lower()).split(' ')[1]
                adress = \
                    list(cursor.execute(
                        f"select distinct address from cinemas where id_cinema = {remember_cinema_num}"))[
                        0][0]
                metro = list(
                    cursor.execute(f"select distinct metro from cinemas where id_cinema = {remember_cinema_num}"))[0][0]
                films = list(
                    cursor.execute(f"select distinct name from cinemas where id_cinema = {remember_cinema_num}"))
                films1 = []
                for i in films:
                    films1.append(i[0])
                films_end = []
                films_ids = []
                films_dict = {}
                for i, e in enumerate(films1, 1):
                    films_end.append(f'{i}) {e}')
                    films_ids.append(str(i))
                    films_dict[str(i)] = e
                this_cinema_name = list(
                    cursor.execute(f"select name_theather from cinemas where id_cinema = '{remember_cinema_num}'"))
                c = ''
                for i in films_end:
                    c += i + '\n'
                vk.method("messages.send", {"peer_id": id,
                                            "message": f"Напиши 'фильм' и его номер в списке для продложения. \n Пример: фильм 228 \n {this_cinema_name[0][0]} \n Адрес: {adress} \n Метро: {metro[1:-1]} \n Список фильмов: \n {c}",
                                            "random_id": random.randint(1, 2147483647)})

            elif main_id == 1 and str(body.lower()).count(' ') == 1 and (str(body.lower()).split(' ')[1] in films_ids) and (
                    str(body.lower()).split(' ')[0] == 'фильм'):
                remember_film_num = str(body.lower()).split(' ')[1]
                film_name = films_dict[remember_film_num]
                age = list(cursor.execute(f"select distinct age from cinemas where name = '{film_name}'"))[0][0]
                time2d = list(cursor.execute(
                    f"select time2d from cinemas where id_cinema = '{remember_cinema_num}' and name = '{film_name}'"))[
                    0][0]
                time3d = list(cursor.execute(
                    f"select time3d from cinemas where id_cinema = '{remember_cinema_num}' and name = '{film_name}'"))[
                    0][0]
                black2d = list(cursor.execute(
                    f"select BLACKtime from cinemas where id_cinema = '{remember_cinema_num}' and name = '{film_name}'"))[
                    0][0]
                karod = list(cursor.execute(
                    f"select discounttime from cinemas where id_cinema = '{remember_cinema_num}' and name = '{film_name}'"))[
                    0][0]
                vk.method("messages.send",
                          {"peer_id": id,
                           "message": f"{film_name}, {age} \n 2D: {time2d[1:-1]} \n 3D: {time3d[1:-1]} \n BLACK 2D: {black2d[1:-1]} \n КАРОакция: {karod[1:-1]} \n Можешь выбрать другой фильм или поздороваться со мной еще раз ",
                           "random_id": random.randint(1, 2147483647)})



            elif body.lower()[:-2] == "посмотреть кинотеатры" and body.lower()[-1] == '2':
                main_id = 2
                cinemas_lst = list(cursor1.execute("select distinct name_theater from cinemas1"))
                cinemas_ids = list(cursor1.execute("select distinct id_cinema from cinemas1"))
                cinemas_lst1 = []
                cinemas_ids1 = []
                for i in cinemas_lst:
                    cinemas_lst1.append(i[0])
                for i in cinemas_ids:
                    cinemas_ids1.append(str(i[0]))
                cinemas_end = []
                for i, e in enumerate(cinemas_lst1, 1):
                    cinemas_end.append(f'{i}) {e}')
                c = ''
                for i in cinemas_end:
                    c += i + '\n'
                vk.method("messages.send",
                          {"peer_id": id,
                           "message": f"Напиши 'кинотеатр' и его номер в списке для продложения. \n Пример: кинотеатр 228 \n Список кинотеатров сети КАРО: \n {c} ",
                           "random_id": random.randint(1, 2147483647)})

            elif str(body.lower()).count(' ') == 1 and (str(body.lower()).split(' ')[1] in cinemas_ids1) and (str(body.lower()).split(' ')[0] == 'кинотеатр') and main_id == 2:
                remember_cinema_num = str(body.lower()).split(' ')[1]
                adress = \
                    list(cursor1.execute(
                        f"select distinct address from cinemas1 where id_cinema = {remember_cinema_num}"))[
                        0][0]
                films = list(
                    cursor1.execute(f"select distinct name_film from cinemas1 where id_cinema = {remember_cinema_num}"))
                films1 = []
                for i in films:
                    films1.append(i[0])
                films_end = []
                films_ids = []
                films_dict = {}
                for i, e in enumerate(films1, 1):
                    films_end.append(f'{i}) {e}')
                    films_ids.append(str(i))
                    films_dict[str(i)] = e
                this_cinema_name = list(
                    cursor1.execute(f"select name_theater from cinemas1 where id_cinema = '{remember_cinema_num}'"))
                c = ''
                for i in films_end:
                    c += i + '\n'
                vk.method("messages.send", {"peer_id": id,
                                            "message": f"Напиши 'фильм' и его номер в списке для продложения. \n Пример: фильм 228 \n {this_cinema_name[0][0]} \n Адрес: {adress} \n Список фильмов: \n {c}",
                                            "random_id": random.randint(1, 2147483647)})

            elif main_id == 2 and str(body.lower()).count(' ') == 1 and (str(body.lower()).split(' ')[1] in films_ids) and (
                    str(body.lower()).split(' ')[0] == 'фильм'):
                remember_film_num = str(body.lower()).split(' ')[1]
                film_name = films_dict[remember_film_num]
                age = list(cursor1.execute(f"select distinct age from cinemas1 where name_film = '{film_name}'"))[0][0]
                time = list(cursor1.execute(
                    f"select time from cinemas1 where id_cinema = '{remember_cinema_num}' and name_film = '{film_name}'"))
                price = list(cursor1.execute(
                    f"select price from cinemas1 where id_cinema = '{remember_cinema_num}' and name_film = '{film_name}'"))
                mode = list(cursor1.execute(
                    f"select mode from cinemas1 where id_cinema = '{remember_cinema_num}' and name_film = '{film_name}'"))
                c = ''
                for i in range(len(time)):
                    c += 'Время: ' + time[i][0] + ' ' + 'Цена: ' + price[i][0][1:-1] + 'Формат: ' + mode[i][0] + '\n'
                vk.method("messages.send",
                          {"peer_id": id,
                           "message": f"{film_name}, {age} \n {c} \n Можешь выбрать другой фильм или поздороваться со мной еще раз ",
                           "random_id": random.randint(1, 2147483647)})

            else:
                vk.method("messages.send", {"peer_id": id, "message": "я не знаю что значит " + str(body.lower()),
                                            "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        time.sleep(1)
