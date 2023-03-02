import config
import telebot
import instagram_parser as ip
import threading


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

def check_new_stories():
	try:
		threading.Timer(7200, check_new_stories).start()
		print('Запускаю плановое обновление')
		x = ip.check_stories()
		print(f"Сделал плановое обновление, количество обновлений: {x}")
	except KeyboardInterrupt:
		print('Заканчиваю программу')

check_new_stories()


bot.infinity_polling(timeout=60, long_polling_timeout = 10)