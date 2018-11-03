import os

from django.core.checks import Error, register, CRITICAL, Tags
from django.conf import settings


@register
def settings_YANDEX_SPEECH_API_KEY(*a, **kw):
    errors = []

    # check for yandex speech key
    if not hasattr(settings, 'YANDEX_SPEECH_API_KEY') or len(settings.YANDEX_SPEECH_API_KEY) == 0:
        errors.append(Error('You must specify YANDEX_SPEECH_API_KEY settings.',
                            hint='Obtain it here: https://developer.tech.yandex.ru/'
                            ))
    return errors
