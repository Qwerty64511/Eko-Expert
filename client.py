import json
import os

import redis
import telebot
from telebot import types

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

redis_url = os.environ.get('REDIS_URL')

dict_db = {}
local = {}
vajnoe = {}
razdel = 'Выбрать другой раздел'

local[7] = 'Задать вопрос дежурному специалисту'
local[9] = razdel

MAIN_STATE = 'main'
VOPROS = 'zadaemvopros'
SPEC = 'Вводится вопрос'
chastiye = 'Частые вопросы'

RAZDEL = 'Выбирается раздел'
RAZDEL1 = 'Выбран раздел 1, выбирается вопрос'
RAZDEL2 = 'Выбран раздел 2, выбирается вопрос'
RAZDEL3 = 'Выбран раздел 3, выбирается вопрос'
RAZDEL4 = 'Выбран раздел 4, выбирается вопрос'
RAZDEL5 = 'Выбран раздел 5, выбирается вопрос'


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

                vajnoe[1] = data
                vajnoe[2] = 'verno'

            else:

                data = json.loads(raw_data)  # выводим нашу базу данных
                print('Viveli')
                vajnoe[1] = data
            local[1] = True

    if local[1]:
        data = vajnoe[1]
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


def change_data(key, user_id, value):
    data = vajnoe['4']
    data[key][user_id] = value

    if redis_url is None:

        json.dump(data,
                  open('db/data.json', 'w', encoding='utf-8'),
                  indent=2,
                  ensure_ascii=False,
                  )
        print('changed', data['states'][user_id])

    else:

        redis_db = redis.from_url(redis_url)
        redis_db.set('data', json.dumps(data))


@bot.message_handler(content_types=['text'])
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

    elif state == SPEC:
        specialist(message)

    elif state == VOPROS:
        vopros(message)

    elif state == chastiye:
        chast(message)


def main_handler(message):
    obnovlenie()

    voprosi = vajnoe['1']
    peremennie = vajnoe['3']
    data = vajnoe['4']
    user_id = str(message.from_user.id)

    if message.text == '/start':

        tekct1 = 'Приветствую, я бот компании Экоэксперт, у меня вы можете узнать ответы на часто задаваемые вопросы. '
        tekct2 = 'Нажав на кнопку вы увидите список частых вопросов'
        tekct = tekct1 + tekct2

        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton('Частые вопросы')
        markup.row(btn1)

        bot.send_message(user_id, tekct, reply_markup=markup)

    elif message.text.lower() == 'задать вопрос дежурному специалисту':

        bot.send_message(user_id, 'Введите ваш вопрос')
        change_data('states', user_id, SPEC)

    elif message.text.lower() == 'частые вопросы':

        change_data('states', user_id, chastiye)
        chast(message)

    elif message.text.lower() == 'выбрать раздел':
        chast(message)


def chast(message):
    obnovlenie()

    user_id = str(message.from_user.id)

    t1 = 'Раздел 1'  # data['razdel'][1]
    t2 = 'Раздел 2'  # data['razdel'][2]
    t3 = 'Раздел 3'  # data['razdel'][3]
    t4 = 'Раздел 4'  # data['razdel'][4]
    t5 = 'Раздел 5'  # data['razdel'][5]

    razdel = 'Выбрать другой раздел'

    local[2] = t1
    local[3] = t2
    local[4] = t3
    local[5] = t4
    local[6] = t5
    local[9] = razdel

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=t1, callback_data=t1)
    btn2 = types.InlineKeyboardButton(text=t2, callback_data=t2)
    btn3 = types.InlineKeyboardButton(text=t3, callback_data=t3)
    btn4 = types.InlineKeyboardButton(text=t4, callback_data=t4)
    btn5 = types.InlineKeyboardButton(text=t5, callback_data=t5)

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    markup.add(btn5)

    question = 'Выберите раздел'
    bot.send_message(user_id, text=question, reply_markup=markup)

    local[user_id] = RAZDEL


@bot.callback_query_handler(func=lambda call: True)
def razdel(call):
    obnovlenie()

    print('HELLO')
    print(RAZDEL)

    user_id = str(call.from_user.id)

    data = vajnoe['4']
    state = data['states'][user_id]
    try:
        local[user_id]

    except KeyError:

        change_data('states', user_id, MAIN_STATE)
        local[user_id] = ' '

    if local[user_id] == RAZDEL:

        print('verno')
        print(call.data)
        print(local)
        voprosi = vajnoe['1']

        raz = data['raz'][user_id]

        a = 2
        print(str(raz))
        b = data['peremennie'][str(raz)]

        while a <= b:

            print('CALL DATA: ' + call.data)

            if call.data in local[a]:

                print('PRIVET')

                t1 = local[2]
                t2 = local[3]
                t3 = local[4]
                t4 = local[5]
                t5 = local[6]
                spec = local[7]

                user_id = str(call.from_user.id)  # Задаём user_id

                if call.data == t1:
                    print('Meniayu1')
                    change_data('states', user_id, RAZDEL1)

                    raz = 1
                    data['raz'][user_id] = raz

                    razdel1(call)

                if call.data == t2:
                    print('Meniayu2')
                    change_data('states', user_id, RAZDEL1)

                    raz = 2
                    data['raz'][user_id] = raz

                    razdel1(call)

                if call.data == t3:
                    print('Meniayu3')
                    change_data('states', user_id, RAZDEL1)

                    raz = 3
                    data['raz'][user_id] = raz

                    razdel1(call)

                if call.data == t4:
                    print('Meniayu4')
                    change_data('states', user_id, RAZDEL1)

                    raz = 4
                    data['raz'][user_id] = raz

                    razdel1(call)

                if call.data == t5:
                    print('Meniayu5')
                    change_data('states', user_id, RAZDEL1)

                    raz = 5
                    data['raz'][user_id] = raz

                    razdel1(call)

                if call.data == spec:
                    bot.send_message(user_id, 'Введите ваш вопрос')
                    change_data('states', user_id, SPEC)

                call.data = 'Анти бесконечно'
                local[user_id] = ' '
            a += 1
            print('norm')

    elif call.data == local[9]:

        print('qwe')
        obnovlenie()

        user_id = str(call.from_user.id)

        t1 = 'Раздел 1'  # data['razdel'][1]
        t2 = 'Раздел 2'  # data['razdel'][2]
        t3 = 'Раздел 3'  # data['razdel'][3]
        t4 = 'Раздел 4'  # data['razdel'][4]
        t5 = 'Раздел 5'  # data['razdel'][5]

        spec = 'Задать вопрос дежурному специалисту'
        razdel = 'Выбрать другой раздел'

        local[2] = t1
        local[3] = t2
        local[4] = t3
        local[5] = t4
        local[6] = t5
        local[7] = spec
        local[9] = razdel

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=t1, callback_data=t1)
        btn2 = types.InlineKeyboardButton(text=t2, callback_data=t2)
        btn3 = types.InlineKeyboardButton(text=t3, callback_data=t3)
        btn4 = types.InlineKeyboardButton(text=t4, callback_data=t4)
        btn5 = types.InlineKeyboardButton(text=t5, callback_data=t5)

        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        markup.add(btn4)
        markup.add(btn5)

        question = 'Выберите раздел'
        bot.send_message(user_id, text=question, reply_markup=markup)

        print('TEST')
        local[user_id] = RAZDEL
        change_data('states', user_id, RAZDEL1)

    else:

        print('else')
        obrabotka(call)


def razdel1(call):
    print('razdel1')

    user_id = str(call.from_user.id)  # Задаём user_id и state
    data = vajnoe['4']

    raz = data['raz'][user_id]

    data = vajnoe['4']
    state = data['states'][user_id]

    razdel = 'Выбрать другой раздел'
    razdel = local[9]

    print(data['razdel'][str(raz)]['voprosi'])

    t1 = data['razdel'][str(raz)]['voprosi']['1']
    t2 = data['razdel'][str(raz)]['voprosi']['2']
    t3 = data['razdel'][str(raz)]['voprosi']['3']
    t4 = data['razdel'][str(raz)]['voprosi']['4']
    t5 = data['razdel'][str(raz)]['voprosi']['5']

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=t1, callback_data=t1)
    btn2 = types.InlineKeyboardButton(text=t2, callback_data=t2)
    btn3 = types.InlineKeyboardButton(text=t3, callback_data=t3)
    btn4 = types.InlineKeyboardButton(text=t4, callback_data=t4)
    btn5 = types.InlineKeyboardButton(text=t5, callback_data=t5)
    btn6 = types.InlineKeyboardButton(text=razdel, callback_data=razdel)

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    markup.add(btn5)
    markup.add(btn6)

    question = 'Выберите Вопрос'
    bot.send_message(user_id, text=question, reply_markup=markup)


def obrabotka(call):
    user_id = str(call.from_user.id)
    data = vajnoe['4']

    raz = data['raz'][user_id]

    user_id = str(call.from_user.id)

    print('CALL DATA: ' + call.data)

    a = 1
    kol = data['peremennie'][str(raz)]

    while a <= kol:

        if call.data == str(data['razdel'][str(raz)]['voprosi'][str(a)]):

            tekct = 'Вопрос: ' + str(data['razdel'][str(raz)]['voprosi']['5']) + ' Ответ: ' + str(
                data['razdel'][str(raz)]['otveti'][str(a)])

            bot.send_message(user_id, tekct)

            change_data('states', user_id, MAIN_STATE)

        a += 1

    tekct0 = ' Вы можете ознакомиться с другими вопросами, выбрав другой раздел. '
    tekct1 = '\nЕсли вы не нашли интересующий вас вопрос, то вы можете задать вопрос специалисту, '
    tekct2 = 'нажав на соответсвующую кнопку.'
    tekct = tekct0 + tekct1 + tekct2

    spec = 'Задать вопрос дежурному специалисту'

    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    btn1 = spec
    btn2 = 'Частые вопросы'
    btn3 = 'Выбрать раздел'

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(user_id, tekct, reply_markup=markup)

    print('obrabotka end')

    print('STATE: ' + str(data['states'][user_id]))


def vopros(message):
    voprosi = vajnoe['1']
    otveti = vajnoe['2']

    user_id = str(message.from_user.id)

    if message.text.lower() == 'задать вопрос дежурному специалисту':

        bot.send_message(user_id, 'Введите ваш вопрос')
        change_data('states', user_id, SPEC)

    elif message.text.lower() == 'частые вопросы':

        chast(message)

    else:
        main_handler(message)


def specialist(message):
    user_id = str(message.from_user.id)
    peremennie = vajnoe['3']

    vopr = message.text
    peremennie['5'] = vopr

    print(peremennie['5'])

    bot.send_message(user_id, 'Если у вас имеются ещё вопросы, то напишите его номер')
    peresilka(message)

    change_data('states', user_id, VOPROS)

    obnovlenie()


def peresilka(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    btn2 = types.KeyboardButton('Частые вопросы')
    markup.row(btn2)

    bot.send_message(message.from_user.id, 'Мы приняли ваш вопрос, в течение коротчайшего времени '
                                           'с вами свяжется специалист', reply_markup=markup)

    chat_id = '-1001202319159'
    bot.forward_message(chat_id, message.chat.id, message.message_id)


bot.infinity_polling()
