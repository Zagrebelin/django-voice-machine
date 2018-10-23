from django.conf.urls import url

from .views import DashView, Mp3Filenames

urlpatterns = [
    url('^get_mp3_files.json', Mp3Filenames.as_view()),
    url('^$', DashView.as_view()),
]