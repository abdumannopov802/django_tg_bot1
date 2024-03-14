from django.shortcuts import render
from django.http import HttpResponse
import telebot
from telebot import types
import logging
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz
import random


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
    if message.from_user.last_name != None:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} {message.from_user.last_name} 😀 \n\n In this bot you can answer simple math questions. \n If you need /help click here.""")
    else:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} 😀 \n\n In this bot you can answer simple math questions. \n If you need /help click here.""")


@bot.message_handler(commands=['help'])
def help_response(message):
    bot.send_message(message.chat.id, 
                     f"""
The following commands are availabe:

/start -> Welcome message
/help -> Show Available Commands
/report -> Report This Bot
/quiz -> Start Quiz
...""")


# Assuming Quiz is your model
questions = [(quiz.question, quiz.answer) for quiz in Quiz.objects.all()]
random.shuffle(questions)

def generate_quiz():
    # Randomly select 5 questions that have not been used before
    return iter_quiz(random.sample(questions, 5))

def iter_quiz(random_quiz_list: list):
    for question, answer in random_quiz_list:
        yield question, answer


@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    user_data = {'step': 1, 'score': 0, 'quiz_iterator': generate_quiz()}
    sending_quiz(message, user_data)

def sending_quiz(message, user_data: dict):
    if user_data['step'] <= 5:
        try:
            question, answer = next(user_data['quiz_iterator'])
            bot.send_message(message.chat.id, f"Question {user_data['step']}:\n{question}")
            bot.register_next_step_handler(message, lambda msg: checking_answer(msg, answer, user_data))
        except StopIteration:
            bot.send_message(message.chat.id, "No more questions available.")
    else:
        bot.send_message(message.chat.id, f"Quiz completed! Your final score: {user_data['score']}/5")

def checking_answer(message, correct_answer, user_data):
    user_answer = message.text.strip().lower()  # Converting to lowercase for case-insensitive comparison
    if user_answer == correct_answer.lower():
        user_data['score'] += 1
        bot.reply_to(message, "Correct! Well done! 👍")
    else:
        bot.reply_to(message, f"Incorrect! The correct answer is: {correct_answer}")

    user_data['step'] += 1
    sending_quiz(message, user_data)
