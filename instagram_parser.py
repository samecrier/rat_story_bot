import config
from instagrapi import Client
import csv
import os
import re
import requests
import config
from random import randint
from datetime import datetime, time
from random import randint
import pytz

# random_agent = ['google', 'redfin', 'Pixel 5', 'qcom', '1080x2340', '440', '12', '31', '244.1.0.19.110', '384108453']
# s_local = 'en_US'
# s_country = 'US'
# this_timezone = 30600

cl = Client()
cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)

def send_to_telegram(filename, format):

	filename = f'C:\\Users\\saycry\\YandexDisk\\Projects\\rat_story_bot\\aleshinaa\\{filename}'

	if format == 'jpg':
		apiURL = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendPhoto'
		photo = open(filename, 'rb')

		parameters = {
			"chat_id" : config.ID_CHANNEL,
		}
		
		files = {
			"photo" : photo
		}

		try:
			response = requests.get(apiURL, data = parameters, files = files)
			print(response.text)
		except Exception as e:
			print(e)

	if format == 'mp4':
		apiURL = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendVideo'
		video = open(filename, 'rb')

		parameters = {
			"chat_id" : config.ID_CHANNEL,
		}
		
		files = {
			"video" : video
		}

		try:
			response = requests.get(apiURL, data = parameters, files = files)
			print(response.text)
		except Exception as e:
			print(e)
	
	print('отправил фото в телеграм!')

def send_sticker_to_telegram():

	rat_stickers = os.listdir('sticker')
	rat_stickers.remove('sticker_special')

	moscow_time_zone = pytz.timezone('Europe/Moscow')
	moscow_time = datetime.now(tz=moscow_time_zone)
	moscow_time = moscow_time.time()

	if moscow_time <= time(7,00):
		sticker = 'sticker_special\\rat_sleep.webp'
	elif moscow_time <= time(10,00):
		sticker = 'sticker_special\\rat_morning.webp'
	else:
		sticker = rat_stickers[randint(0,36)]

	filename = f'C:\\Users\\saycry\\YandexDisk\\Projects\\rat_story_bot\\sticker\\{sticker}'

	apiURL = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendSticker'
	sticker = open(filename, 'rb')

	parameters = {
		"chat_id" : config.ID_CHANNEL,
	}
	
	files = {
		"sticker" : sticker
	}

	try:
		response = requests.get(apiURL, data = parameters, files = files)
		print(response.text)
	except Exception as e:
		print(e)


def check_stories():
	print('начинаю проверять')

	user_id = cl.user_id_from_username("aleshina.alena.k")
	user_stories = cl.user_stories(user_id)

	sticker_checker = 0
	count_of_stories = 0

	for index, story in enumerate(user_stories):
		insta_dict = dict((item, value) for item, value in story)
		with open('aleshinaa/datas/data.csv', 'r', encoding='utf-8', newline='') as f:
			csv_reader = csv.DictReader(f, delimiter=',')
			for row in csv_reader:
				if row['id'] == insta_dict['id']:
					break
			else:
				count_of_stories =+ 1
				names_of_content = os.listdir('aleshinaa')
				names_of_content = sorted([int(re.sub(r'(.*)\.(.*)', r'\1', row)) for row in names_of_content if (re.sub(r'(.*)\.(.*)', r'\1', row)).isdigit()])
				if names_of_content == []:
					filename = 1
				else:
					filename = names_of_content[-1]+1
				insta_dict['filename'] = filename
				cl.story_download(story.pk, filename=filename, folder="aleshinaa")
				with open('aleshinaa/datas/data.csv', 'a', newline='', encoding='utf-8') as f:
					writer = csv.DictWriter(f, fieldnames=insta_dict.keys())
					writer.writerow(insta_dict)
				if sticker_checker == 0:
					send_sticker_to_telegram()
					sticker_checker += 1
				names_of_content = os.listdir('aleshinaa')
				if insta_dict['video_url'] == None:
					filename_format = f'{filename}.jpg'
					send_to_telegram(filename_format, format='jpg' )
				else:
					filename_format = f'{filename}.mp4'
					send_to_telegram(filename_format, format='mp4')

	print('я обновил сториз!')
	return count_of_stories
