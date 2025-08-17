import telebot
from telebot import types
import webbrowser
from datetime import date
import sqlite3

from unicodedata import category

bot = telebot.TeleBot('8200144246:AAHHqWfLpkQsZhQehDjPyX1GORdbu4Egiq4')

users_data = {}

@bot.message_handler(commands = ['start'])
def start(message):
    # file = open('./Screenshot.jpg', 'rb')
    # bot.send_message(message.chat.id, 'Hello!')
    # bot.send_photo(message.chat.id, file)
    if message.from_user.id not in users_data:
        users_data[message.from_user.id] = []
        bot.send_message(message.chat.id, 'Привет! 👋 \nЯ зарегистрировал Вас в системе учета расходов')
    else:
        bot.send_message(message.from_user.id, 'С возращением! \nВы уже зарегистривованы')

@bot.message_handler(commands = ['hello'])
def main(message):
    bot.send_message(message.chat.id, f'Hello! {message.from_user.first_name} {message.from_user.last_name}')

@bot.message_handler(commands = ['help'])
def main(message):
    bot.send_message(message.chat.id, 'Этот бот предназначен для удобного отслеживания и контроля ваших расходов.')

@bot.message_handler(commands = ['site', 'website'])
def site(message):
    webbrowser.open('https://github.com/sergeilubimkov/tg-bot')

@bot.message_handler(commands = ['add'])
def site(message):
    args = message.text.split()[1:]
    if len(args) < 2:
        bot.reply_to(message, 'Извините, Вы некорректно ввели команду.\nИспользуйте, пожалуйста, синтаксиси вида:\n/add сумма категория')
        return

    try:
        amount = float(args[0])
    except ValueError:
        bot.reply_to(message, 'Извините, Вы ошиблись\nСумма должна быть числом.\nИспользуйте, пожалуйста, синтаксиси вида:\n/add сумма категория')
        return

    category = ' '.join(args[1:])
    users_data[message.from_user.id].append({'amount': amount, 'category': category, 'date': date.today()})
    bot.send_message(message.from_user.id, f'✅ Добавлено: {amount} руб на {category}')

@bot.message_handler(commands = ['today'])
def today(message):
    user_id = message.from_user.id
    today_date = date.today()

    expenses = [e for e in users_data.get(user_id, []) if e["date"] == today_date]

    if not expenses:
        bot.send_message(message.from_user.id, "Сегодня расходов пока нет")
        return

    totals_by_category = {}
    for e in expenses:
        category = e["category"]
        totals_by_category[category] = totals_by_category.get(category, 0) + e["amount"]

    lines = [f"- {amount} руб. ({category})" for category, amount in totals_by_category.items()]

    details = "\n".join(lines)
    total = sum(totals_by_category.values())

    bot.send_message(message.from_user.id, f"Сегодняшние расходы:\n{details}\n\nИтого: {total} руб.")


@bot.message_handler(content_types = ['photo', 'video', 'audio', 'voice', 'document', 'video_note'])
def get_file(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавить пожелания', url='https://github.com/sergeilubimkov/tg-bot'))
    #region TestingButton
    btn1 = types.InlineKeyboardButton('Удалить файл', callback_data='delete')
    # btn2 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn1) #, btn2)
    #endregion
    bot.reply_to(message, 'Извините, я пока что не умею обрабатывать файлы \nВы можете оставить свои пожелания по ссылке ниже:', reply_markup = markup)

#region TestingButton
@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.edit_message_text('Файл удалён', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('Изменил текст', callback.message.chat.id, callback.message.message_id)
#endregion

@bot.message_handler()
def info(message):
    if message.text.lower() == 'id':
        bot.reply_to(message, f'Your ID: {message.from_user.id}')
    if message.text.lower() == 'hello':
        bot.reply_to(message, f'Hello! {message.from_user.first_name} {message.from_user.last_name}')

bot.infinity_polling()