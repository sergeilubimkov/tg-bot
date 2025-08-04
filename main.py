import telebot

bot = telebot.TeleBot('8200144246:AAHHqWfLpkQsZhQehDjPyX1GORdbu4Egiq4')

@bot.message_handler(commands = ['start'])
def main(message):
    bot.send_message(message.chat.id, 'Hello!')

@bot.message_handler(commands = ['hello'])
def main(message):
    bot.send_message(message.chat.id, f'Hello! {message.from_user.first_name} {message.from_user.last_name}')

@bot.message_handler(commands = ['help'])
def main(message):
    bot.send_message(message.chat.id, 'help')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'id':
        bot.reply_to(message, f'Your ID: {message.from_user.id}')
    if message.text.lower() == 'hello':
        bot.reply_to(message, f'Hello! {message.from_user.first_name} {message.from_user.last_name}')

bot.infinity_polling()