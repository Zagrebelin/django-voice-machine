import os

from django.core.management import BaseCommand
from django.conf import settings
import telebot, telebot.types
from telebot.types import Message
import requests

from ...tools import talk
from ...models import ScheduleItem

bot = telebot.TeleBot('337231177:AAEJprXTPG9h0GlYfqdwuE0gN7F-aJyTkv4')


def access_filter(func):
    def inner_function(*a, **kw):
        return func(*a, **kw)

    return inner_function


@bot.message_handler(content_types=['voice'])
@access_filter
def play_audio(message):
    file = bot.get_file(message.voice.file_id)  # type: telebot.types.File
    file_path = file.file_path
    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
    file_name = os.path.normpath(os.path.join(settings.YANDEX_SPEECH_CACHE_PATH, file_path))
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    rsp = requests.get(file_url, stream=True)
    with open(file_name, 'wb') as f:
        for data in rsp.iter_content(chunk_size=4096):
            f.write(data)
    settings.OGG_PLAYER([file_name])
    bot.reply_to(message, file_url)


@bot.message_handler(commands=['say'])
@access_filter
def say(message: Message):
    text = message.text.split(' ', 1)
    if len(text) == 1:
        return
    text = text[1]
    if text.split()[0] in ['primary', 'secondary']:
        voice_type, text = text.split(' ', 1)
    else:
        voice_type = 'primary'

    if text.split()[0] in ['normal', 'neutral', 'good', 'evil']:
        emotion, text = text.split(' ', 1)
        emotion = 'neutral' if emotion == 'normal' else emotion
    else:
        emotion = 'neutral'
    item = ScheduleItem(voice_type=voice_type, voice_emotion=emotion, message=text)
    talk([item])
    bot.reply_to(message, 'done.')


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.polling()

        # TODO: подсказки для команды say
        # TODO: access_filter
