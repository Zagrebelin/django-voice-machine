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


@register
def settings_YANDEX_SPEECH_CACHE_PATH(*a, **kw):
    if not hasattr(settings, 'YANDEX_SPEECH_CACHE_PATH') or len(settings.YANDEX_SPEECH_CACHE_PATH) == 0:
        return [Error('You must specify YANDEX_SPEECH_CACHE_PATH path.')]

    path = settings.YANDEX_SPEECH_CACHE_PATH
    if not os.path.exists(path):
        return [Error(f'Cache path {path} not found.')]

    try:
        tmpname = os.path.join(path, 'abcd')
        open(tmpname, 'w').close()
        os.unlink(tmpname)
    except IOError:
        return [Error(f'Unable write to cache path {path}')]
    return []

@register
def settings_MP3_PLAYER(*a, **kw):
    if not hasattr(settings, 'MP3_PLAYER'):
        return [Error('MP3_PLAYER settings must be defined.',
                      hint='It is a callable with *filenames args')]
    if not callable(settings.MP3_PLAYER):
        return [Error('MP3_PLAYER settings must be callable.',
                      hint='It is a callable with *filenames args')]
    return []
