from django.shortcuts import render

# Create your views here.
import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import telebot
import logging
from .models import Post

TOKEN = '7088062989:AAF9kDgwFxyYd_fgLr2fwbtcaulmBc7vg5c'

URL = 'https://3efd-213-230-88-239.ngrok.io/getpost/'

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'

bot = telebot.TeleBot(TOKEN)

def setwebhook(request):
  response = requests.post(TELEGRAM_API_URL+ "setWebhook?url=" + URL)
  return HttpResponse(f"{response}")

@csrf_exempt
def index(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponse("Telegram Bot")
    if request.method == 'POST':
        update = telebot.types.Update.de_json(
            request.body.decode("utf-8"))
        try:
            bot.process_new_updates([update])
        except Exception as e:
            logging.error(e)
        return HttpResponse(status=200)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Nima haqida ma'lumot olishni istaysiz?")
    print(message)

@bot.message_handler(content_types=['text'])
def echo_all(message):
    data:Post
    data = Post.objects.all()
    kitobdef = {}
    for i in data:
        kitobdef[i.title] = i.content

    if message.text in kitobdef:
        bot.reply_to(message, kitobdef[message.text])
    else:
        bot.reply_to(message, "Uzur siz so'ragan ma'lumot hozircha mavjud emas!")