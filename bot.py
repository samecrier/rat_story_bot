import config
import telebot
from instagrapi import Client
import config
import os




bot = telebot.TeleBot(config.BOT_TOKEN)




@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):

	for filename in os.listdir('aleshinaa'):
		if 'jpg' in filename:
			content = open(f"aleshinaa/{filename}", 'rb')
			bot.send_photo(message.chat.id, content)
		elif 'mp4' in filename:
			content = open(f"aleshinaa/{filename}", 'rb')
			bot.send_video(message.chat.id, content)
# 	cl = Client()
# 	cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)

# # print('one')

# 	user_id = cl.user_id_from_username("aleshina.alena.k")
# 	user_stories = cl.user_stories(user_id)

# 	stories_pk = []

# 	for index, story in enumerate(user_stories):
# 		cl.story_download(story.pk, filename= f"{index}", folder="aleshinaa")


	








bot.infinity_polling()