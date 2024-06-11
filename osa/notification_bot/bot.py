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
    bot.send_message(message.chat.id, "<b>Добро пожаловать\n"
                     "🛎️Это бот по отправлению уведомлений о посещениях на тренировку.\n"
                     "📨Бот будет уведомлять Вас о приходе и уходе вашего ребенка с тренировки</b>", parse_mode="HTML")
    bot.send_message(message.chat.id,
                     "Для того чтобы начать получать уведомления, Вам необходимо себя <b>идентифицировать</b>👤\n\n"
                     "Введите свой номер телефона. \n"
                     "<b>Номер должен начинаться с +7 и не включает пробелов</b>.\n✅ПРИМЕР +79237846644 ✅",
                     parse_mode="HTML")
    bot.register_next_step_handler(message, callback=check_mobile_phone)


def check_mobile_phone(message):
    payload = {
        'mobile_phone': message.text,
        'chat_id': message.chat.id
    }
    response = requests.post(URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        ls = ''.join([f' {child}\n' for child in data["data"].get("children")])

        bot.send_message(message.chat.id, f' Ваше ФИО <b> {data["data"].get("parent")}</b>',
                         parse_mode="HTML")
        bot.send_message(message.chat.id, f'ФИО Ваших детей:\n<b>{ls}</b>', parse_mode="HTML")
        bot.send_message(message.chat.id, '🎉🎉Теперь Вы будете получать уведомления о посещениях')
    else:
        ...
        #Дописать логику


def send_notification(message, chat_id):
    bot.send_message(chat_id, message, parse_mode="HTML")




if __name__ =="__main__":
    bot.polling()




