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
import logging
from moviepy.editor import *
import openai
import config
import pytesseract
from PIL import Image
import cv2
import pytesseract
import re


# random_agent = ['google', 'redfin', 'Pixel 5', 'qcom', '1080x2340', '440', '12', '31', '244.1.0.19.110', '384108453']
# s_local = 'en_US'
# s_country = 'US'
# this_timezone = 30600

login_number = 0

def send_to_telegram(filename, format, caption=None):

	filename = f'C:\\Users\\saycry\\YandexDisk\\Projects\\rat_story_bot\\aleshinaa\\content\\{filename}'

	if format == 'jpg':
		apiURL = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendPhoto'
		photo = open(filename, 'rb')

		parameters = {
			"chat_id" : config.ID_CHANNEL,
			"caption" : caption
		}
		files = {
			"photo" : photo
		}

		try:
			response = requests.get(apiURL, data = parameters, files = files)
			logging.info(response.text)
		except Exception as e:
			logging.exception(e)

	if format == 'mp4':
		apiURL = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendVideo'
		video = open(filename, 'rb')

		parameters = {
			"chat_id" : config.ID_CHANNEL,
			"caption" : caption
		}

		files = {
			"video" : video
		}

		try:
			response = requests.get(apiURL, data = parameters, files = files)
			logging.info(response.text)
		except Exception as e:
			logging.exception(e)
	logging.info('отправил фото в телеграм!')

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
		logging.info(response.text)
	except Exception as e:
		logging.exception(e)

def mp4_to_mp3(filename):
	video = VideoFileClip(f"aleshinaa/content/{filename}.mp4")
	mp3_filename = f"aleshinaa/audio/{filename}.mp3"
	try:
		video.audio.write_audiofile(mp3_filename, verbose=False, logger=None)
	except AttributeError:
		return None
	openai.api_key = config.OPENAI_API_KEY
	audio_file = open(mp3_filename, "rb")
	transcript = openai.Audio.transcribe("whisper-1", audio_file)
	transcript_final = transcript['text']
	return transcript_final.encode('utf-8').decode()


def text_transcription(img, size=500):
	pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
	scale_percent = int(size)# Процент от изначального размера
	image = cv2.imread(img)
	width = int(image.shape[1] * scale_percent / 100)
	height = int(image.shape[0] * scale_percent / 100)
	dim = (width, height)
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	text = pytesseract.image_to_string(gray, lang="rus+eng")
	text = re.sub(r'\n\n', r'\n', text)
	return text


def check_stories():
	logging.info('начинаю проверять')
	cl = Client()
	cl.request_timeout = randint(5, 20)
	# cl.set_proxy('http://chentcovru:qR2siEhkJ2@108.165.218.104:50100')
	global login_number
	try:
		cl.load_settings('settings/dump.json')
		cl.get_timeline_feed()
		login_number += 1
		logging.info(f'Количество входов в инстаграм в текущем сеансе: {login_number}')
	except Exception as e:
		print(f'{datetime.now()} // ошибка входа в инстаграм по json, пытаюсь зайти через логин-пароль.')
		logging.warning('------------------------------Не загрузилась настройка json------------------------------')
		logging.exception(e)
		try:
			new_settings = {}
			cl.set_settings(new_settings)
			cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD, relogin=True)
			cl.get_timeline_feed()
			cl.dump_settings('settings/dump.json')
			login_number += 1
			logging.info(f'Количество входов в инстаграм в текущем сеансе: {login_number}')
		except Exception as e:
			print(f'{datetime.now()} // не удалось зайти в инстаграм')
			logging.critical('Не удалось зайти в инстаграм')
			logging.exception(e)

	user_id = cl.user_id_from_username("aleshina.alena.k")
	user_stories = cl.user_stories(user_id)
	sticker_checker = 0
	count_of_stories = 0

	for story in user_stories:
		insta_dict = dict((item, value) for item, value in story)
		with open('aleshinaa/datas/data.csv', 'r', encoding='utf-8', newline='') as f:
			csv_reader = csv.DictReader(f, delimiter=',')
			for row in csv_reader:
				if row['id'] == insta_dict['id']:
					break
			else:
				count_of_stories += 1
				names_of_content = os.listdir('aleshinaa/content')
				names_of_content = sorted([int(re.sub(r'(.*)\.(.*)', r'\1', row)) for row in names_of_content if (re.sub(r'(.*)\.(.*)', r'\1', row)).isdigit()])
				if names_of_content == []:
					filename = 1
				else:
					filename = names_of_content[-1]+1
				insta_dict['filename'] = filename
				cl.story_download(story.pk, filename=filename, folder="aleshinaa/content")
				if sticker_checker == 0:
					send_sticker_to_telegram()
					sticker_checker += 1
				names_of_content = os.listdir('aleshinaa/content')
				if insta_dict['video_url'] == None:
					filename_format = f'{filename}.jpg'
					image_transcription = text_transcription(f'aleshinaa/content/{filename_format}')
					insta_dict['transcription'] = [image_transcription]
					send_to_telegram(filename_format, format='jpg', caption=image_transcription)
				else:
					filename_format = f'{filename}.mp4'
					mp4_transcription = mp4_to_mp3(filename)
					insta_dict['transcription'] = [mp4_transcription]
					send_to_telegram(filename_format, format='mp4', caption=mp4_transcription)
				with open('aleshinaa/datas/data.csv', 'a', newline='', encoding='utf-8') as f:
					writer = csv.DictWriter(f, fieldnames=insta_dict.keys())
					writer.writerow(insta_dict)

	logging.info('я обновил сториз!')
	return count_of_stories
