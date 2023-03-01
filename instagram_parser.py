import config
from instagrapi import Client
import csv
import os
import re
from collections import defaultdict
import requests
import config
from time import sleep

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

	filename = f'C:\\Users\\saycry\\YandexDisk\\Projects\\rat_story_bot\\sticker\\rat.webp'

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
	cl = Client()
	cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)


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
