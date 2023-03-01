import config
import telebot
import instagram_parser as ip
from time import sleep


bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer_to_message(message):
	positive_results = ['обнови', 'алешина', 'алёшина', 'инст', 'давай']
	if message.text.lower() in positive_results:
		bot.reply_to(message, 'Я проверяю обновления')
		x = ip.check_stories()
		if x == 0:
			bot.reply_to(message, 'Нет новых обновлений')
		elif x == 1:
			bot.reply_to(message, f"Добавлено {x} новое обновление")
		else:
			bot.reply_to(message, f"Добавлено {x} новых обновлений")
	else:
		bot.reply_to(message, 'Использую одно из слов чтобы обновить ленту: обнови, алешина, алёшина, инст, давай')


bot.infinity_polling(timeout=60, long_polling_timeout = 10)