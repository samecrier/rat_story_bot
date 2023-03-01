import config
import telebot
import instagram_parser as ip

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer_to_message(message):
	positive_results = ['обнови', 'алешина', 'алёшина', 'инст', 'давай']
	if message.text.lower() in positive_results:
		bot.reply_to(message, 'Я проверяю обновления')
		ip.check_stories()
		bot.reply_to(message, 'Я добавил все новые обновления')
	else:
		bot.reply_to(message, 'Использую одно из слов чтобы обновить ленту: обнови, алешина, алёшина, инст, давай')



bot.infinity_polling()