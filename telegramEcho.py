import telebot
import sys

bot = telebot.TeleBot(sys.args[1])
running = false

@bot.message_handler(commands=['start'])
def send_welcome(message):
	global running
	bot.reply_to(message, "I will start echoing messages. Write /exit to stop me.")
	running = true

@bot.message_handler(commands=['exit'])
def stop_running(message):
	global running
	bot.reply_to(message, "I will stop echoing messages. Write /start to start again.")
	running = false

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	if running:
		bot.reply_to(message, message.text)

bot.polling()