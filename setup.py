import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-voice-machine',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django', 'requests', 'lxml'],
    author='Pavel Zagrebelin',
    author_email='pavel@zagrebelin.ru',
    description='A Django application to time-based voice announcments',
    url='https://zagrebelin.ru/voice-machine/',
)
