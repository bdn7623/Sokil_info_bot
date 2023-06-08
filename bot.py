# t.me/Sokil_info_bot

import telebot
import sqlite3
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)

bottons = ['Лікарня','Інтернет','Ремонт','Комунальні служби','Крамниці/послуги','Заявка на додавання','Інше']

doctors = [
    '🩺 Поліклініка на Соколі (тимчасово на Перемозі) \n ☎ 067-747-68-54',
    '🩺 Ковязина ☎ 067-771-67-60',
    '🩺 Сальников ☎ 068-299-94-30',
    '👩‍ Реєстратура на пр. Героїв 22 ☎ 068-299-95-37',
    '🩻 Поліклініка на Тополі ☎ 098-328-41-14',
    '🦷 Стомат реєстратура на Перемозі ☎ 068-883-34-26',
    '🐈 Вветеринарна клініка на Соколі ☎ 097-555-74-39 \n Айболітна ☎ 068-046-83-9'
            ]

provaiders = {
    'Київстар':'Тех підтримка: 0-800-300-460 \n https://kyivstar.ua/support',
    'Укртелеком':'Тех підтримка: 0-800-506-800  \n https://ukrtelecom-internet.com.ua/taryfy-internet',
    'Gigabit by Vega':'Тех підтримка: 0 800 60 45 96 \n https://gigabit.vega.ua/',
    'Vega':'Тех підтримка: 0 800 60 00 60, +38 (099) 177 50 50 \n https://vega.ua/ukr/contacts',
    'Фрегат':'(056) 734-44-44 \n(063) 734-44-44 \n(098) 734-44-44 \n(099) 734-44-44 \n https://fregat.com/about/contacts/',
    'Triolan':'Тех підтримка: (093) 172-16-16,\n(096) 720-15-15,\n(095) 233-15-15\n https://triolan.com/contacts.aspx?lng=ru&reg=dn',
    'Воля':'Тех підтримка: 050-502-22-50\n 068-502-22-50\n 093-502-22-50\n https://volia.com/ukr/dnipro/internet/?partner=organic_search&utm_source=google&utm_medium=organic',
    'Союз Телеком':'Тех підтримка: 0 800 750 114  \n https://www.soyuz.in.ua/ua/contact.html',
    'DTS':'Viber: +380 (73) 71-99-000\n Email: dts@dts.net.ua\n https://dts.net.ua/contacts/'
}

remonts = {
    'Сантехнік':'🛁\n ☎ 097-207-48-22 👨 Микола Гаврилович',
    'Електрик':'💡\n ☎ 096-790-69-01 👨 Анатолій Олександрович \n ☎ 095-671-28-22 👨 Славик',
    'Холодильник':'☎ 063-798-21-56, 098-651-82-88, 099-620-33-90 👨 Андрій Вікторович',
    'Пральна машина':'☎ 097-99-00-520 \n ☎ 095-413-18-19 👨 Олексій',
    'Посудомійна машина':'☎ (097) 887-93-88',
    'Мікрохвильовка':'☎ (099) 921-40-31, (093) 921-40-31, (067) 921-40-31',
    'Телевізор':'📺 \n ☎ 066 100 5432, 063 796 9243 \n Володимир ☎ 067-336-21-27, 063-796-74-25',
    'Бойлер':'☎ 067-788-22-33 \n ☎ 095-413-18-19 👨 Олексій \n 📞 067-132-68-10',
    'Ремонт одягу':'👖 👗 Ремонт одягу ☎ 050-690-86-98 👱‍♀Ольга'
}

kom_sersices = {
'Ліфтер':'Дніпроліфт на ж/м Сокіл ☎ 066-724-26-43, 050-781-83-28 \n Ліфт dp ua  ☎ 066-080-32-02',
'Aварійна служба':'Міська аварійна служба (цілодобово) ☎ (056) 736-10-02 ',
'Дніпрогаз':'Дніпрогаз ☎ (056) 745-23-55, (056) 78-78-104, (067) 62-63-104 \n https://dpgor.dsoua.com/ua/',
'ДТЭК':'ДТЭК ☎ 790-99-00, (066) 790-99-00, (067) 790-99-00, (063) 790-99-00 \n https://www.dtek-dnem.com.ua/ua',
'Дніпроводоканал':'☎ 745-55-65, 745-90-64 \n https://vodokanal.dp.ua/kontakti/',
'Теплоенерго':'☎ (056) 374-30-18, (056) 374-30-08',
'Дніпркомунтранс':'Дніпркомунтранс (Уберу) ☎ +38 067 622 81 88, +38 056 776 57 63 /n https://uberu.dp.ua/#rec276144859',
'КП «Зооконтроль»':'☎ (067) 908-89-86, (068) 828-22-55',
'Міськзеленбуд':'Міськзеленбуд ☎ (098) 036-73-05'
}

shops = {
    'Домашня випічка':"🍰 торти, пряники та інше ☎ 095-609-09-15  \n 🎂 торти ☎ 095-490-27-91 Марина",
    'Манікюр':'💅 Оксана \n☎ 095-788-96-14 \nСокіл-2, бул. Слави, буд. 30, корп. 2, кв. 21'
}

@bot.message_handler(commands=["start"])
def start_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for number, element in enumerate(bottons, 1):
        locals()["botton" + str(number)] = f"botton{number}"
        button = types.KeyboardButton(text=element)
        button_width = len(element) * 2  # Розрахунок ширини кнопки на основі довжини тексту
        button.button_width = button_width
        row.append(button)

        if len(row) == 2:  # Якщо рядок містить 2 кнопки
            markup.row(*row)  # Додати рядок кнопок до розмітки
            row = []  # Очистити список для наступного рядка

    if row:  # Якщо залишилися кнопки в останньому неповному рядку
        markup.row(*row)  # Додати останній рядок кнопок до розмітки

    bot.send_message(message.chat.id,
                     'Вітаю, {0.first_name}! \nЯ Сокіл_Інфо_Бот. \nОберіть потрібний розділ:'.format(message.from_user),
                     reply_markup=markup)
    registration(message)


def registration(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER UNIQUE,
        user_first_name TEXT,
        user_last_name TEXT
    )""")

    people_id = message.chat.id
    people_firstname = message.chat.first_name
    people_lastname = message.chat.last_name
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        purchases = [(people_id),
                     (people_firstname),
                     (people_lastname)]
        cursor.execute("INSERT INTO login_id VALUES(?,?,?)", purchases)
        connect.commit()

def create_bottons(message, dict_read):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('Назад')
    row = []

    for number, element in enumerate(dict_read, 1):
        locals()["botton" + str(number)] = f"botton{number}"
        button = types.KeyboardButton(text=element)
        button_width = len(element) * 3
        button.button_width = button_width
        row.append(button)

        if len(row) == 3:
            markup.row(*row)
            row = []

    if row:
        markup.row(*row)

    markup.row(back)
    bot.send_message(message.chat.id, 'Оберіть: ', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Лікарня':
            for doctor in doctors:
                bot.send_message(message.chat.id, doctor)

        elif message.text == 'Інтернет':
            create_bottons(message, dict_read=provaiders)

        if message.text in provaiders:
            bot.send_message(message.chat.id, provaiders.get(message.text))

        elif message.text == 'Ремонт':
            create_bottons(message, dict_read=remonts)

        if message.text in remonts:
            bot.send_message(message.chat.id, remonts.get(message.text))

        elif message.text == 'Комунальні служби':
            create_bottons(message, dict_read=kom_sersices)

        if message.text in kom_sersices:
            bot.send_message(message.chat.id, kom_sersices.get(message.text))

        elif message.text == 'Крамниці/послуги':
            create_bottons(message, dict_read=shops)

        if message.text in shops:
            bot.send_message(message.chat.id, shops.get(message.text))

        elif message.text == 'Інше':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, 'Нажаль, пусто', reply_markup=markup)

        elif message.text == 'Заявка на додавання':
            bot.send_message(message.chat.id, '✍ Запит на додавання інформації')
            bot.send_message(message.chat.id, 'Надішліть, наприклад: \n вид послуги \n ім"я \n номер телефону \n тощо')
            sent = bot.reply_to(message, "Чeкаю")
            bot.register_next_step_handler(sent, review)

        elif message.text == 'Назад':
            start_action(message)

def review(message):
    first_name = message.chat.first_name
    message_admin = message.text
    print(message_admin)
    admin_id = (os.getenv("my_id"))
    bot.send_message(admin_id, f"Надійшов запит від @{first_name} !\n"
                               f"Текст: \n"
                               f"{message_admin}")
    bot.send_message(message.chat.id, 'Заявку відправлено')

    connect = sqlite3.connect('users_text.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_first_name TEXT,
        text TEXT
    )""")

    user_id = message.chat.id
    user_first_name = message.chat.first_name
    user_message = message.text

    cursor.execute("INSERT INTO user_messages (user_id, user_first_name, text) VALUES (?, ?, ?)",
                   (user_id, user_first_name, user_message))
    connect.commit()

    start_action(message)

bot.polling(none_stop=True)