from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import telebot

bot = telebot.TeleBot('1592562907:AAGdFFwaQ2f6QotTEuWeYFs3PohgsEHvuiE', threaded=False)


@csrf_exempt
def bot_view(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    if request.META.get('CONTENT_TYPE') != 'application/json':
        return HttpResponse(status=403)

    json_string = request.body.decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])

    return HttpResponse(status=200)



