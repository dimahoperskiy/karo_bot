import requests
from bs4 import BeautifulSoup
import re
import copy
import sqlite3

# karo

def remove_all(string):
    pattern = re.compile(r'[А-Яа-яёЁ0-9 ]+')
    return pattern.findall(string)[0].strip()


def remove_alcal2(string):
    pattern = re.compile(r'[A-Za-z0-9 ]+')
    return pattern.findall(string)[0].strip()


def find_all_theaters_KARO(theatres):
    dicti = {}
    metro_class = 'cinemalist__cinema-item__metro__station-list__station-item'
    for theater in theatres:
        dicti[theater.findAll('h4')[0].text.strip()] = {
            'metro': [remove_all(i.text) for i in theater.findAll('li', class_=metro_class)],
            'address': theater.findAll('p')[0].text.split('+')[0].strip(),
            'phone': '+' + theater.findAll('p')[0].text.split('+')[-1],
            'data-id': theater['data-id']
        }
    return dicti


def modes_and_time(film_num, siteid):
    url_theaters_id = url_theaters + '?id='
    # url1 = url_theaters_id + '1' + '&date=2019-12-08'
    # url1 = str(url_theaters_id) + str(siteid) + '&date=2019-12-09'
    url1 = str(url_theaters_id) + str(siteid)
    m = requests.get(url1)
    m.text
    soup2 = BeautifulSoup(m.text, "html.parser")
    shit = soup2.findAll('div', class_='cinema-page-item__schedule__row__board-table')
    modes_list = []
    dictt = {}
    for i in range(len(shit[film_num].findAll('div', class_='cinema-page-item__schedule__row__board-row__left'))):
        mode = shit[film_num].findAll('div', class_='cinema-page-item__schedule__row__board-row__left')[i].text
        pattern = re.compile(r'[А-Яа-яёЁ0-9A-Za-z ]+')
        modes = pattern.findall(mode)
        for k in range(len(modes)):
            modes[k] = modes[k].strip()
            modes_list.append(modes[k])

        time = shit[film_num].findAll('div', class_='cinema-page-item__schedule__row__board-row__right')[i].text
        pattern = re.compile(r'[0-9]+:[0-9]+')
        dictt[modes[k]] = {
            'time': pattern.findall(time)
        }
    return (dictt)


def all_films():
    lol = 100 // len(find_all_theaters_KARO(theatres))
    ans = find_all_theaters_KARO(theatres)
    cnt2 = 0
    for theatre in find_all_theaters_KARO(theatres):
        url_theaters_id = url_theaters + '?id='
        # url1 = url_theaters_id + find_all_theaters_KARO(theatres)[theatre]['data-id'] + '&date=2019-12-09'
        # print(find_all_theaters_KARO(theatres)[theatre]['data-id'])
        # url1 = url_theaters_id + '3' + '&date=2019-12-08'
        url1 = url_theaters_id + find_all_theaters_KARO(theatres)[theatre]['data-id']
        dataid = find_all_theaters_KARO(theatres)[theatre]['data-id']

        m = requests.get(url1)
        m.text

        dictf = {}

        if m.status_code == 200:
            soup1 = BeautifulSoup(m.text, "html.parser")
            films = soup1.findAll('div', class_='cinema-page-item__schedule__row__inner')
            # karo_theatres = find_all_theaters_KARO(theatres)
        else:
            print("Страница не найдена")

        cnt = 0
        for film in films:
            # print(film.findAll('h3')[0].text)
            film.findAll('h3')[0].text.split(',')[0]

            # for i in range(len(film.findAll('a'))):
            # print(film.findAll('a')[i].text)

            dictf[film.findAll('h3')[0].text.split(',')[0].rstrip()] = {
                'age': film.findAll('h3')[0].text.split(',')[1],
                'modes': modes_and_time(cnt, dataid)
            }
            cnt += 1
        ans[theatre].setdefault('films', dictf)
    return ans


url = "https://karofilm.ru"
url_theaters = url + "/theatres"

r = requests.get(url_theaters)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    theatres = soup.findAll('li', class_='cinemalist__cinema-item')
    karo_theatres = find_all_theaters_KARO(theatres)
else:
    print("Страница не найдена")

answer1 = all_films()
answer = copy.deepcopy(answer1)
for a, b in enumerate(answer1):
    for c, d in enumerate(answer1[b]):
        for e, f in enumerate(answer1[b]['films']):
            for g, h in enumerate(answer1[b]['films'][f]):
                for i, j in enumerate(answer1[b]['films'][f]['modes']):
                    if '2D' in answer1[b]['films'][f]['modes'].keys():
                        pass
                    else:
                        answer[b]['films'][f]['modes']['2D'] = {'time': ''}

                    if '3D' in answer1[b]['films'][f]['modes'].keys():
                        pass
                    else:
                        answer[b]['films'][f]['modes']['3D'] = {'time': ''}

                    if 'BLACK 2D' in answer1[b]['films'][f]['modes'].keys():
                        pass
                    else:
                        answer[b]['films'][f]['modes']['BLACK 2D'] = {'time': ''}

                    if 'КАРОакция' in answer1[b]['films'][f]['modes'].keys():
                        pass
                    else:
                        answer[b]['films'][f]['modes']['КАРОакция'] = {'time': ''}

conn = sqlite3.connect('KARO2.db')
cursor = conn.cursor()

cursor.execute('drop table cinemas')

cursor.execute("""CREATE TABLE cinemas(
                id integer PRIMARY KEY,
                id_cinema integer,
                name_theather text,
                name text,
                age text,
                time2d text,
                time3d text,
                BLACKtime text,
                discounttime text,
                metro text,
                address text
                )""")
conn.commit()

base = answer
id1_ = 0
filmes = 'films'
metroes = 'metro'
address = 'address'
modes = 'modes'
twod = '2D'
threed = '3D'
black = 'BLACK 2D'
disc = 'КАРОакция'
age = 'age'
time = 'time'
for b in base:
    id1_ += 1
    for f in base[b]['films']:
        qwe = re.sub("'", ' ', f)
        xy = re.sub('"', '', base[b][address])
        time2 = str(base[b][filmes][f][modes][twod][time])
        time3 = str(base[b][filmes][f][modes][threed][time])
        blck = str(base[b][filmes][f][modes][black][time])
        discc = str(base[b][filmes][f][modes][disc][time])
        time2 = re.sub("'", "", time2)
        time3 = re.sub("'", "", time3)
        blck = re.sub("'", "", blck)
        discc = re.sub("'", "", discc)
        cursor.execute(
            f'insert or replace into cinemas(id_cinema, name_theather, name, metro, address, time2d, time3d, BLACKtime, discounttime, age) values({id1_}, "{b}", "{qwe}", "{base[b][metroes]}", "{xy}", "{time2}", "{time3}", "{blck}", "{discc}", "{base[b][filmes][f][age]}")')
conn.commit()

# mirage cinema

url = 'http://moscow.mirage.ru/cinemas/cinemas.htm'
r = requests.get(url)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    theatres = soup.findAll('div', class_='alltheaters')
else:
    print("Страница не найдена")

mirage = {}
for i, e in enumerate(theatres):
    for k in range(3):
        mirage[theatres[i].findAll('a')[k].text] = {'adress': '',
                                                    'films': {}
                                                    }
work = []
for i, e in enumerate(theatres):
    a = theatres[i].select('div.alltheaters a')
    for t in a:
        work.append('http://moscow.mirage.ru' + t.attrs['href'])

adresses = []
for i in work:
    url = i
    r = requests.get(url)
    if r.status_code == 200:
        soup1 = BeautifulSoup(r.text, "html.parser")
        adress = soup1.findAll('div', class_='half lt')
        a = re.sub('(\r)|(\n)|(\t)|(\tr)', '', adress[0].findAll('h4')[0].text)
        adresses.append(a)
    else:
        print("Страница не найдена")

for i, e in enumerate(mirage):
    mirage[e]['adress'] = adresses[i]

for theatre in work:
    r = requests.get(theatre)
    if r.status_code == 200:
        soup2 = BeautifulSoup(r.text, "html.parser")
        theatres = soup2.findAll('td', class_='col2')

    else:
        print("Страница не найдена")

    name = soup2.findAll('div', class_='fix')

    for i in range(1, len(theatres)):
        a = soup2.findAll('td', class_='col1')
        c = soup2.findAll('td', class_='col6')
        e = soup2.findAll('td', class_='col3')
        lenn = len(c[i].findAll('span', class_='price'))
        film_name = re.sub('(\r)|(\n)|(\t)', '', theatres[i].findAll('a')[0].text)

        b = str(a[i])
        p = re.compile(r'[0-9]+[:][0-9]+')
        film_time = (p.findall(b)[0] + '-' + p.findall(b)[1])

        prices = []
        for k in range(lenn):
            d = c[i].findAll('span', class_='price')[k].text
            d = re.sub('(\n)|(\t)|(\r)', '', d)
            prices.append(d)
        price = prices

        price = [n for n in price if n]

        mode = e[i].find('i')['title']
        if e[i].find('i')['title'] == 'Цифровой':
            mode = '2D'
        elif e[i].find('i')['title'] == 'Трехмерная':
            mode = '3D'
        if film_name in list(mirage[name[2].findAll('h1')[0].text]['films'].keys()):
            mirage[name[2].findAll('h1')[0].text]['films'][film_name]['time'].setdefault(film_time,
                                                                                         {'price': price, 'mode': mode})

        else:
            mirage[name[2].findAll('h1')[0].text]['films'][film_name] = {}
            mirage[name[2].findAll('h1')[0].text]['films'][film_name]['time'] = {}
            a = soup2.findAll('td', class_='col4')
            b = re.sub(r'(\r)|(\t)|(\n)', '', a[i].findAll('span')[0].text)
            mirage[name[2].findAll('h1')[0].text]['films'][film_name]['age'] = b
            mirage[name[2].findAll('h1')[0].text]['films'][film_name]['time'].setdefault(film_time,
                                                                                         {'price': price, 'mode': mode})

conn1 = sqlite3.connect('mirage4.db')
cursor1 = conn1.cursor()

cursor1.execute('drop table cinemas1')

cursor1.execute("""CREATE TABLE cinemas1(
                id integer PRIMARY KEY,
                id_cinema integer,
                name_theater text,
                address text,
                name_film text,
                age text,
                time text,
                price text,
                mode text
                )""")
conn1.commit()

base = mirage
cinema_id = 1
for b in base:
    adress_mir = base[b]['adress']
    for d in base[b]['films']:
        age_mir = base[b]['films'][d]['age']
        for f in base[b]['films'][d]['time']:
            mode_mir = base[b]['films'][d]['time'][f]['mode']
            price_mir = base[b]['films'][d]['time'][f]['price']
            cursor1.execute(
                f'insert or replace into cinemas1(id_cinema, name_theater, address, name_film, age, time, price, mode) values ("{cinema_id}" ,"{b}", "{adress_mir}", "{d}", "{age_mir}", "{f}", "{price_mir}", "{mode_mir}")')

    cinema_id += 1
conn1.commit()

