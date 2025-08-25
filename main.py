import telebot
import os
from dotenv import load_dotenv
from telebot import types
import webbrowser
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
import insert_into_DB
import forDB
from unicodedata import category

load_dotenv()
forDB.init_db()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

users_data = {}

@bot.message_handler(commands = ['start'])
def start(message):

    if not insert_into_DB.check_users(message.from_user.id):
        insert_into_DB.add_user(message.from_user.id)
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
    insert_into_DB.add_expenses(message.from_user.id, amount, category)
    bot.send_message(message.from_user.id, f'✅ Добавлено: {amount} руб на {category}')

def send_expenses_report(message, expenses, total, title, empty_text):
    if not expenses:
        bot.send_message(message.from_user.id, empty_text)
        return

    lines = ""
    for amount, category in expenses:
        lines += f"- {float(amount):.2f} руб. ({category})\n"

    text = f"{title}:\n{lines}\nИтого: {total:.2f} руб."
    bot.send_message(message.from_user.id, text)

@bot.message_handler(commands = ['today'])
def today(message):
    user_id = message.from_user.id

    expenses, total = insert_into_DB.today_expenses(user_id)
    send_expenses_report(
        message, expenses, total,
        "Сегодняшние расходы",
        "Сегодня расходов пока нет"
    )

@bot.message_handler(commands = ['yesterday'])
def yesterday(message):
    user_id = message.from_user.id

    expenses, total = insert_into_DB.yesterday_expenses(user_id)
    send_expenses_report(
        message, expenses, total,
        "Вчерашние расходы",
        "Вчера расходов не было"
    )

@bot.message_handler(commands = ['week'])
def week(message):
    user_id = message.from_user.id

    expenses, total = insert_into_DB.week_expenses(user_id)
    send_expenses_report(
        message, expenses, total,
        "Расходы за последнюю неделю",
        "За последнюю неделю расходов не было"
    )

@bot.message_handler(commands = ['month'])
def month(message):
    user_id = message.from_user.id

    expenses, total = insert_into_DB.month_expenses(user_id)
    send_expenses_report(
        message, expenses, total,
        "Расходы за последний месяц",
        "За последний месяц расходов не было"
    )


@bot.message_handler(content_types = ['photo', 'video', 'audio', 'voice', 'document', 'video_note'])
def get_file(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавить пожелания', url='https://github.com/sergeilubimkov/tg-bot'))
    #region TestingButton
    btn1 = types.InlineKeyboardButton('Удалить файл', callback_data='delete')
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

def send_reminder():
    USER_IDS = insert_into_DB.getUsers()
    for user_id in USER_IDS:
        bot.send_message(user_id, "👋 Не забудьте внести сегодняшние расходы!")

scheduler = BackgroundScheduler()

scheduler.add_job(send_reminder, 'cron', hour=21, minute=0)
scheduler.start()

bot.infinity_polling()