import config
import telebot
import instagram_parser as ip
import threading
import logging
import random

logging.basicConfig(
	level=logging.INFO, 
	handlers=[logging.FileHandler(filename='datas/logs/file.log', encoding='utf-8')],
	format = "%(asctime)s // %(levelname)-8s // %(filename)-20s : %(lineno)-4d // %(message)s"
)

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer_to_message(message):
	positive_results = ['обнови', 'алешина', 'алёшина', 'инст', 'давай']
	if message.text.lower() in positive_results:
		bot.reply_to(message, 'Я проверяю обновления')
		logging.info(f'Боту отправили: "{message.text}", я начал проверять обновления')
		x = ip.check_stories()
		if x == 0:
			bot.reply_to(message, 'Нет новых обновлений')
			logging.info('Ответил, что нет новых обновлений')
		elif x == 1:
			bot.reply_to(message, f"Добавлено {x} новое обновление")
			logging.info(f'Ответил, что добавил одно новое обновление')
		else:
			bot.reply_to(message, f"Добавлено {x} новых обновлений")
			logging.info(f'Ответил, что добавил {x} новых обновлений')
	else:
		bot.reply_to(message, 'Используй одно из слов, чтобы обновить ленту: обнови, алешина, алёшина, инст, давай')
		logging.info(f'Отправили неверное сообщение "{message.text}"')

def check_new_stories():
	try:
		time_options = [i for i in range(7200, 14400)]
		threading.Timer(random.choice(time_options), check_new_stories).start()
		logging.info('Запускаю плановое обновление')
		x = ip.check_stories()
		logging.info(f"Сделал плановое обновление, количество обновлений: {x}")
	except KeyboardInterrupt:
		logging.info('Заканчиваю программу')

check_new_stories()

bot.infinity_polling(timeout=60, long_polling_timeout = 10)