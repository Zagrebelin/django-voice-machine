import datetime
import os
import random
import re


def date_as_string(dt: datetime.datetime) -> str:
    day_list = ['', 'первое', 'второе', 'третье', 'четвёртое',
                'пятое', 'шестое', 'седьмое', 'восьмое',
                'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
                'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
                'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
                'двадцать первое', 'двадцать второе', 'двадцать третье',
                'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
                'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
                'тридцатое', 'тридцать первое']
    month_list = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    day = day_list[dt.day]
    month = month_list[dt.month]
    return f'{day} {month}'


def time_as_string(dt: datetime.datetime) -> str:
    """
    :param dt:
    :return:
    """
    t = dt.strftime('%H:%M')
    ret = None
    hum_name = os.path.join(os.path.dirname(__file__), 'humanize_testdata.txt')
    with open(hum_name, 'r', encoding='utf8') as f:
        for l in f:
            if l.split('-')[0].strip() != t:
                continue
            vars = list(map(str.strip, l.split('-')[1].split(',')))
            ret = random.choice(vars)
            break
    if not ret:
        hour_s = decline(dt.hour, 'часов', 'час', 'часа')
        min_s = decline(dt.minute, 'минут', 'минута', 'минуты')
        minute = int_to_str(dt.minute, 'female')
        hour = int_to_str(dt.hour, 'male')
        ret = f'{hour} {hour_s} {minute} {min_s}'
    ret = re.sub('\d+', repl=lambda m: int_to_str(int(m.group(0))), string=ret)
    return ret


def weekday_as_string(dt: datetime.datetime) -> str:
    return 'понедельник вторник среда четверг пятница суббота воскресенье'.split()[dt.weekday()]


def int_to_str(i: int, gender: str = 'male') -> str:
    """

    :param i:
    :param gender: MALE FEMALE or MIDDLE
    :return:
    """
    decs = ['', 'десять', 'двадцать', 'тридцать', 'сорок', 'пятьдесят']
    ones = {
        'male': 'ноль один два три четыре пять шесть семь восемь девять'.split(),
        'female': 'ноль одна две три четыре пять шесть семь восемь девять'.split(),
        'middle': 'ноль одно два три четыре пять шесть семь восемь девять'.split()
    }
    ones = ones[gender.lower()]
    tens = 'одиннадцать двенадцать тринадцать четырнадцать пятнадцать шестнадцать семнадцать восемнадцать девятнадцать'.split()
    dec, one = divmod(i, 10)
    if dec == 0:
        return ones[one]
    if one == 0:
        return decs[dec]
    if dec == 1:
        return tens[one - 1]
    return f'{decs[dec]} {ones[one]}'


def decline(num, zero, one, two):
    if (num % 100) // 10 == 1 or num % 10 in (0, 5, 6, 7, 8, 9):
        return zero
    if num % 10 == 1:
        return one
    return two
