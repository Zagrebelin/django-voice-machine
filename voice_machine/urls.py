from django.conf.urls import url

from .views import DashView, mp3_filenames

urlpatterns = [
    url('^get_mp3_files.json', mp3_filenames, name='mp3-files'),
    url('^$', DashView.as_view()),
]