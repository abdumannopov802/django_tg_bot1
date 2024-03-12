from django.shortcuts import render
from django.http import HttpResponse
import telebot
from telebot import types
import logging
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

TOKEN = '7057271752:AAGKvkuVz_7fl5z_9PbUuzG7ZWigZ8kcOgE'

bot = telebot.TeleBot(TOKEN)

def index(request):
    return HttpResponse("Hello guys")

@csrf_exempt
def bot_view(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode("utf-8"))
        try:
            bot.process_new_updates([update])
        except Exception as e:
            logging.error(e)
        return HttpResponse(status=200)


from .functions import generate_quiz

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('help', callback_data='help')
    btn_2 = types.InlineKeyboardButton('Start Quiz', callback_data='start_quiz')
    markup.add(btn_1, btn_2)

    if message.from_user.last_name != None:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} {message.from_user.last_name} 😀 \n\n In this bot you can answer to simple math questions. \n If you need /help click here.""", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} 😀 \n\n In this bot you can answer simple math questions. \n If you need /help click here.""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data == 'help':
        bot.send_message(call.message.chat.id, f"""The following commands are availabe: \n\n/start -> Welcome message \n/help -> Show Available Commands \n/report -> Report This Bot \n/quiz -> Start Quiz...""")
            
    else:
        user_data = {'step':1, 'score':0}
        sending_quiz(call.messsage, user_data)

        def sending_quiz(message, user_data:dict):
            if user_data['step'] <= 5:
                quiz = generate_quiz()
                question, answer = quiz[0], quiz[1]

                bot.send_message(message.chat.id, f"step : {user_data['step']}/5 \n {question}")
                bot.register_next_step_handler(message, lambda msg: checking_answer(msg, answer, user_data))

                def checking_answer(message, correct_answer, user_data):
                    try:
                        user_answer = int(message.text)
                    except ValueError:
                        bot.reply_to(message, "Invalid input 😔. \nPlease be careful! \nYou can restart on click /quiz ...")
                    
                    if user_answer == correct_answer:
                        user_data['score'] += 1

                    user_data['step'] += 1
                    if user_data['step'] == 5+1:
                        bot.send_message(message.chat.id, f"Quiz completed! Your final score: {user_data['score']}/5")
                        return
                    else:
                        sending_quiz(message, user_data)