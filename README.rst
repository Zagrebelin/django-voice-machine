=====
Voice Machine
=====

Voice Machine is a simple Django app to time-based voice announcements.
You can provide time, day of week and text for any message.

This module uses an Yandex SpeechKit (https://tech.yandex.ru/speechkit/cloud/).

Quick start
-----------

1. Add "voice_machine" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'voice_machine',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('voice/', include('voice_machine.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Get Yandex Speech API key here:  https://developer.tech.yandex.ru/ and add to your settings like this::

    YANDEX_SPEECH_API_KEY = 'put your key here'

