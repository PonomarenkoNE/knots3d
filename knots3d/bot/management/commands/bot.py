from django.core.management.base import  BaseCommand
from django.conf import settings
import telebot

from bot.models import Categories, Knot, Favorite


def all_cat(all, is_type):
    lst = list()
    if is_type:
        for el in all:
            lst.append(el.type)
    else:
        for el in all:
            lst.append(el.name)
    return '\n'.join([str(el) for el in lst])


class Command(BaseCommand):
    help = "Telegram-bot"

    def handle(self, *args, **options):
        bot = telebot.TeleBot('1592562907:AAGdFFwaQ2f6QotTEuWeYFs3PohgsEHvuiE')

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, 'hello world')

        @bot.message_handler(commands=['view'])
        def view(message):
            #parsing = message.text.split[' ']
            if True:
                knots = Knot.objects.all()
                cat = Categories.objects.all()
                fav = Categories.objects.all()
                bot.send_message(message.chat.id, f'Full list:\n'
                                                  f'All knots ({len(knots)})\n'
                                                  f'Favorite ({len(fav)})\n'
                                                  f'\n'
                                                  f'Category:\n'
                                                  f'{all_cat(cat, False)}\n'
                                                  f'Type:\n'
                                                  f'{all_cat(cat, True)}\n')

        bot.polling()
