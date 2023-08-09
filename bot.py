# t.me/Sokil_info_bot

import telebot
import sqlite3
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv
from info import * #Уся інформація для назв кнопок та їх зміст

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)

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
        button = types.KeyboardButton(text=element)
        button_width = len(element) * 3
        button.resize_keyboard = button_width
        row.append(button)

        if len(row) == 3:
            markup.row(*row)
            row = []

    if row:
        markup.row(*row)

    markup.row(back)

    bot.send_message(message.chat.id, 'Оберіть: ', reply_markup=markup)

def send_doctors(message):
    for doctor in doctors:
        bot.send_message(message.chat.id, doctor)

def send_category_info(message, category_dict):
    create_bottons(message, dict_read=category_dict)

def send_info_request(message):
    bot.send_message(message.chat.id, '✍ Запит на додавання інформації')
    bot.send_message(message.chat.id, 'Для додавання інформації до Боту, \nнадішліть, наприклад: \n вид послуги \n ім"я \n номер телефону \n тощо')
    sent = bot.reply_to(message, "Чeкаю")
    bot.register_next_step_handler(sent, review)

def start_handler(message):
    start_action(message)

handlers = {
    'Лікарня': send_doctors,
    'Інтернет': lambda message: send_category_info(message, provaiders),
    'Ремонт': lambda message: send_category_info(message, remonts),
    'Комунальні служби': lambda message: send_category_info(message, kom_sersices),
    'Крамниці/послуги': lambda message: send_category_info(message, shops),
    'Інше': lambda message: send_category_info(message, others),
    'Заявка на додавання інформації': send_info_request,
    'Назад': start_handler
}

@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == 'private':
        handler = handlers.get(message.text)
        if handler:
            handler(message)
        elif message.text in provaiders:
            bot.send_message(message.chat.id, provaiders[message.text])
        elif message.text in remonts:
            bot.send_message(message.chat.id, remonts[message.text])
        elif message.text in kom_sersices:
            bot.send_message(message.chat.id, kom_sersices[message.text])
        elif message.text in shops:
            bot.send_message(message.chat.id, shops[message.text])
        elif message.text in others:
            bot.send_message(message.chat.id, others[message.text])

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
