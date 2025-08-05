import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('8200144246:AAHHqWfLpkQsZhQehDjPyX1GORdbu4Egiq4')

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('Посетить сайт')
    btn1 = types.KeyboardButton('Удалить файл')
    btn2 = types.KeyboardButton('Изменить текст')
    markup.add(button)
    markup.row(btn1, btn2)
    file = open('./Screenshot.jpg', 'rb')
    bot.send_message(message.chat.id, 'Hello!', reply_markup = markup)
    bot.send_photo(message.chat.id, file)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Посетить сайт':
        webbrowser.open('https://github.com/sergeilubimkov/tg-bot')
    #elif message.text == 'Удалить файл':
        #bot.delete_message(message.chat.id, message.message_id - 1)
    #elif message.text == 'Изменить текст':
        #bot.edit_message_text('Изменил текст', message.chat.id, message.message_id - 1)

@bot.message_handler(commands = ['hello'])
def main(message):
    bot.send_message(message.chat.id, f'Hello! {message.from_user.first_name} {message.from_user.last_name}')

@bot.message_handler(commands = ['help'])
def main(message):
    bot.send_message(message.chat.id, 'help')

@bot.message_handler(commands = ['site', 'website'])
def site(message):
    webbrowser.open('https://github.com/sergeilubimkov/tg-bot')

@bot.message_handler(content_types = ['photo', 'video', 'audio', 'voice', 'document', 'video_note'])
def get_file(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавить пожелания', url='https://github.com/sergeilubimkov/tg-bot'))
    #region TestingButton
    btn1 = types.InlineKeyboardButton('Удалить файл', callback_data='delete')
    btn2 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn1, btn2)
    #endregion
    bot.reply_to(message, 'Извините, я пока что не умею обрабатывать файлы \n\nВы можете оставить свои пожелания по ссылке ниже:', reply_markup = markup)

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