import json
import os

import redis
import telebot
from telebot import types

token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)
redis_url = os.environ.get('REDIS_URL')

dict_db = {}
vajnoe = {}
local = {}


def obnovlenie():
    print('OBNOVA')

    try:

        local[1]

    except KeyError:

        print('EROR')

        if redis_url is None:

            print('none')

            try:

                data = json.load(open('db/data.json', 'r', encoding='utf-8'))  # выводим нашу базу данных
                vajnoe[1] = data

            except FileNotFoundError:

                data = {
                    "states": {
                    },
                    "voprosi": {},
                    "otveti": {},
                    "raz": {
                    },
                    "peremennie": {
                        "1": {},
                        "2": {},
                        "3": {},
                        "4": {},
                        "5": {}
                    },
                    "zadaemvopros": {},
                    "otvechaem": {},
                    "main": {},
                    "admins": {
                        "mainadmins": "",
                        "Koder": "810391410"
                    },
                    "razdel": {
                        "1": {
                            "voprosi": {
                            },
                            "otveti": {
                            }
                        },
                        "2": {
                            "voprosi": {},
                            "otveti": {}
                        },
                        "3": {
                            "voprosi": {},
                            "otveti": {}
                        },
                        "4": {
                            "voprosi": {},
                            "otveti": {}
                        },
                        "5": {
                            "voprosi": {},
                            "otveti": {}
                        }
                    }
                }

                vajnoe[1] = data
                print(vajnoe[1])
            local[1] = False

        else:

            local[1] = True
            redis_db = redis.from_url(redis_url)
            raw_data = redis_db.get('data')
            print('Viveodim')

            if raw_data is None:

                data = {
                    "states": {
                    },
                    "voprosi": {},
                    "otveti": {},
                    "raz": {
                    },
                    "peremennie": {
                        "1": {},
                        "2": {},
                        "3": {},
                        "4": {},
                        "5": {}
                    },
                    "zadaemvopros": {},
                    "otvechaem": {},
                    "main": {},
                    "admins": {
                        "mainadmins": "",
                        "Koder": "810391410"
                    },
                    "razdel": {
                        "1": {
                            "voprosi": {
                            },
                            "otveti": {
                            }
                        },
                        "2": {
                            "voprosi": {},
                            "otveti": {}
                        },
                        "3": {
                            "voprosi": {},
                            "otveti": {}
                        },
                        "4": {
                            "voprosi": {},
                            "otveti": {}
                        },
                        "5": {
                            "voprosi": {},
                            "otveti": {}
                        }
                    }
                }
                redis_db = redis.from_url(redis_url)
                redis_db.set('data', json.dumps(data))

                vajnoe[1] = data
                vajnoe[2] = 'verno'

            else:

                data = json.loads(raw_data)  # выводим нашу базу данных
                print('Viveli')
                vajnoe[1] = data
                local[1] = True

    if local[1]:
        data = vajnoe[1]
        print('DATA: ' + str(data))
        redis_db = redis.from_url(redis_url)
        redis_db.set('data', json.dumps(data))

    data = vajnoe[1]

    voprosi1 = str(data["razdel"]['1']["voprosi"]) + ' ' + str(data["razdel"]['2']["voprosi"])
    voprosi2 = str(data["razdel"]['3']["voprosi"]) + ' ' + str(data["razdel"]['4']["voprosi"])
    voprosi = voprosi1 + ' ' + voprosi2 + ' ' + str(data["razdel"]['5']["voprosi"])
    otveti = data["razdel"]['1']["otveti"]
    peremennie = data['peremennie']

    vajnoe['1'] = voprosi
    vajnoe['2'] = otveti
    vajnoe['3'] = peremennie
    vajnoe['4'] = data

    if str(voprosi) == '{}':
        kol = 0
        peremennie['0'] = kol


obnovlenie()

MAIN_STATE = 'main'
VOPROS = 'zadaemvopros'
OTVET = 'otvechaem'
ADMIN = 'Идёт администрирование'

RAZDEL = 'Выбирается раздел'
RAZDEL1 = 'Раздел 1'
RAZDEL2 = 'Раздел 2'
RAZDEL3 = 'Раздел 3'
RAZDEL4 = 'Раздел 4'
RAZDEL5 = 'Раздел 5'


def change_data(key, user_id, value):
    obnovlenie()
    data = vajnoe['4']

    data[key][user_id] = value
    # проверяем наличие базы данных на редис

    if redis_url is None:  # Обработка базы данных, если нет подключения к редис
        json.dump(data,
                  open('db/data.json', 'w', encoding='utf-8'),
                  indent=2,
                  ensure_ascii=False,
                  )

    # Загружаем базу данных из редис
    else:

        redis_db = redis.from_url(redis_url)
        redis_db.set('data', json.dumps(data))


@bot.message_handler(content_types=['text'])
def checker(message):
    user_id = str(message.from_user.id)
    data = vajnoe['4']

    if user_id in data['admins']['Koder'] or user_id in data['admins']['mainadmins']:
        dispatcher(message)

    else:
        bot.send_message(user_id, 'Вы не можете пользоваться этим ботом, за доступом обратитесь к @Qwerty64511')


def dispatcher(message):
    obnovlenie()
    data = vajnoe['4']

    user_id = str(message.from_user.id)

    if str(data['states']) == '{}':
        # проверяем наличие пользователей, если их нет,
        # то вызываем функцию добавления пользователя
        change_data('states', user_id, MAIN_STATE)

    try:
        print(data['states'][user_id])

    except KeyError:
        change_data('states', user_id, MAIN_STATE)

    state = data['states'][user_id]
    print('current state', user_id, state)

    if state == MAIN_STATE:
        main_handler(message)

    elif state == OTVET:
        otvet(message)

    elif state == ADMIN:
        adminka(message)

    elif state == RAZDEL:
        razdel(message)

    elif state == RAZDEL1:
        razdel1(message)


def main_handler(message):
    obnovlenie()
    user_id = str(message.from_user.id)
    data = vajnoe['4']
    peremennie = vajnoe['3']

    try:

        raz = data['raz'][user_id]

    except KeyError:

        data['raz'][user_id] = {}

    raz = data['raz'][user_id]

    if message.text == '/start':

        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton('Добавить вопрос')
        btn2 = types.KeyboardButton('Посмотреть все вопросы и ответы к ним')
        markup.row(btn1, btn2)

        tekct = ' Привет, мистер админ в этом боте ты можешь добавлять часто  задаваемые вопросы и вводить на них ответ'
        tekct1 = '\n Доступные комманды:'

        bot.send_message(user_id, tekct + tekct1, reply_markup=markup)

    elif message.text.lower() == 'добавить вопрос':

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        btn1 = 'Раздел 1'
        btn2 = 'Раздел 2'
        btn3 = 'Раздел 3'
        btn4 = 'Раздел 4'
        btn5 = 'Раздел 5'
        markup.row(btn1, btn2, btn3, btn4, btn5)

        bot.send_message(user_id, 'Выберите раздел', reply_markup=markup)
        change_data('states', user_id, RAZDEL)

    elif message.text.lower() == 'посмотреть все вопросы и ответы к ним':

        voprosi = data["razdel"][str(raz)]["voprosi"]
        otveti = data["razdel"][str(raz)]["otveti"]

        print('OTVETI: ' + str(otveti))
        print('Vopros: ' + str(voprosi))

        if str(data["razdel"][str(raz)]["voprosi"]) == '{}':
            kol = 0
            peremennie[str(raz)] = kol

        a = 1
        kol = peremennie[str(raz)]
        print(kol)

        if kol == -1:
            bot.send_message(user_id, 'База вопросов и ответов пуста')

        else:

            while a <= kol:
                markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
                btn1 = types.KeyboardButton('Добавить вопрос')
                btn2 = types.KeyboardButton('Посмотреть все вопросы и ответы к ним')
                markup.row(btn1, btn2)

                tekct = 'Вопрос: ' + voprosi[str(a)] + ' Ответ: ' + otveti[str(a)] + ' Раздел: ' + str(raz)
                bot.send_message(user_id, tekct, reply_markup=markup)
                a += 1

    elif message.text.lower() == 'админ':

        if user_id == data['admins']['Koder']:
            doadmenki = data['states'][user_id]
            local[0] = doadmenki

            markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
            btn1 = 'Очистить БД'
            btn2 = 'Вывод БД'
            markup.row(btn1, btn2)

            bot.send_message(user_id, 'Вход выполнен, выберите команду', reply_markup=markup)
            change_data('states', user_id, ADMIN)

    else:
        bot.send_message(user_id, 'Я вас не понял.')


def razdel(message):
    obnovlenie()
    user_id = str(message.from_user.id)

    data = vajnoe['4']
    peremennie = vajnoe['3']
    raz = data['raz'][user_id]

    if message.text.lower() == 'раздел 1':
        raz = 1
        data['raz'][user_id] = raz

        proverka(message)

        kol = peremennie[str(raz)]

        peremennie[str(raz)] = kol

        bot.send_message(user_id, 'Введите вопрос')
        change_data('states', user_id, RAZDEL1)

    if message.text.lower() == 'раздел 2':
        raz = 2
        data['raz'][user_id] = raz

        proverka(message)

        bot.send_message(user_id, 'Введите вопрос')
        change_data('states', user_id, RAZDEL1)

    if message.text.lower() == 'раздел 3':
        raz = 3
        data['raz'][user_id] = raz

        proverka(message)

        bot.send_message(user_id, 'Введите вопрос')
        change_data('states', user_id, RAZDEL1)

    if message.text.lower() == 'раздел 4':
        raz = 4
        data['raz'][user_id] = raz

        proverka(message)

        bot.send_message(user_id, 'Введите вопрос')
        change_data('states', user_id, RAZDEL1)

    if message.text.lower() == 'раздел 5':
        raz = 5
        data['raz'][user_id] = raz

        proverka(message)

        bot.send_message(user_id, 'Введите вопрос')
        change_data('states', user_id, RAZDEL1)

    if peremennie[str(raz)] == {}:
        kol = 0
        peremennie[str(raz)] = kol


def proverka(message):
    user_id = str(message.from_user.id)

    data = vajnoe['4']
    peremennie = vajnoe['3']
    raz = data['raz'][user_id]

    try:
        kol = peremennie[str(raz)]

    except KeyError:

        kol = 0
        peremennie[str(raz)] = kol


def razdel1(message):
    user_id = str(message.from_user.id)

    peremennie = vajnoe['3']
    data = vajnoe['4']
    raz = data['raz'][user_id]

    data = vajnoe['4']

    kol = peremennie[str(raz)]
    kol = int(kol)
    kol += 1

    data["razdel"][str(raz)]['voprosi'][str(kol)] = message.text

    bot.send_message(user_id, 'Введите ответ')

    change_data('states', user_id, OTVET)

    peremennie[str(raz)] = kol

    obnovlenie()


def otvet(message):
    print('OTVET')

    user_id = str(message.from_user.id)

    data = vajnoe['4']
    raz = data['raz'][user_id]
    peremennie = vajnoe['3']

    prov = {}

    obnovlenie()
    data = vajnoe['4']

    try:

        kol = peremennie[str(raz)]
        prov[1] = True

    except KeyError:

        prov[1] = False
        change_data('states', user_id, MAIN_STATE)
        main_handler(message)

    if prov[1]:

        print('TRUE')
        kol = peremennie[str(raz)]

        data["razdel"][str(raz)]['otveti'][str(kol)] = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        btn1 = 'Посмотреть все вопросы и ответы к ним'
        btn2 = 'Добавить вопрос'
        markup.row(btn1, btn2)

        tekct = 'Вопрос: ' + data["razdel"][str(raz)]['voprosi'][str(kol)] + ' Ответ: '
        tekct = tekct + ' ' + data["razdel"][str(raz)]['otveti'][str(kol)]
        bot.send_message(user_id, tekct, reply_markup=markup)

        if redis_url is None:

            change_data('states', user_id, MAIN_STATE)

        else:

            redis_db = redis.from_url(redis_url)
            redis_db.set('data', json.dumps(data))

            change_data('states', user_id, MAIN_STATE)


def adminka(message):
    user_id = str(message.from_user.id)
    data = vajnoe['4']

    try:
        doadmenki = local[0]

    except KeyError:
        doadmenki = MAIN_STATE

    if message.text.lower() == 'очистить бд':
        a = 1
        b = 5
        while a <= b:
            data['razdel'][str(a)]['voprosi'] = {}
            data['razdel'][str(a)]['otveti'] = {}
            data['peremennie'][str(a)] = {}
            a += 1

        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        btn1 = 'Вывод БД'
        btn2 = 'Выход'
        markup.row(btn1, btn2)

        vajnoe['4'] = data
        bot.send_message(user_id, 'Очистилось', reply_markup=markup)

        vajnoe['4'] = data
        print('VAJNOE  ' + str(vajnoe[1]))

        redis_db = redis.from_url(redis_url)
        redis_db.set('data', json.dumps(data))

        obnovlenie()

    elif message.text.lower() == 'вывод бд':

        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        btn1 = 'выход'
        btn2 = 'очистить БД'
        markup.row(btn1, btn2)

        vopr = data['razdel']

        print(vopr)

        try:

            bot.send_message(user_id, str(data), reply_markup=markup)

        except TypeError:

            bot.send_message(user_id, 'База пустая', reply_markup=markup)
        obnovlenie()

    elif message.text.lower() == 'выход':

        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton('Добавить вопрос')
        btn2 = types.KeyboardButton('Посмотреть все вопросы и ответы к ним')
        markup.row(btn1, btn2)

        bot.send_message(user_id, 'Выход выполнен', reply_markup=markup)
        change_data('states', user_id, doadmenki)
        print(user_id, data['states'])


bot.infinity_polling()
