from dotenv import load_dotenv
import os
import requests
import telebot

load_dotenv()

URL = 'http://0.0.0.0:8000/bot/check_parent_mobile_phone/'
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать\n"
                     "Этот бот отправляет уведомления о приходе и уходе с тренировки.\n"
                     "Чтобы начать получать уведомления Вам необходимо себя идентифицировать!!!\n"
                     "Введите свой номер телефона. Номер должен начинаться с +7 и без пробелов. ПРИМЕР +79237846644")
    bot.register_next_step_handler(message, callback=check_mobile_phone)


def check_mobile_phone(message):
    payload = {
        'mobile_phone': message.text,
        'chat_id': message.chat.id
    }
    response = requests.post(URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        bot.send_message(message.chat.id, f'{data}')
    else:
        ...
        #Дописать логику


def send_notification(message, chat_id):
    bot.send_message(chat_id, message)




if __name__ =="__main__":
    bot.polling()




