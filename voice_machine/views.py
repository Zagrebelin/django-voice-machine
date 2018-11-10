import json

from django.http import HttpResponse, Http404, JsonResponse
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware, utc
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from django.contrib.staticfiles.templatetags.staticfiles import static

from . import models, tools


class DashView(TemplateView):
    template_name = 'dash.html'


@csrf_exempt
def mp3_filenames(request):
    timestr = request.POST.get('dt', None) or request.GET.get('dt', None) or None
    if not timestr:
        raise Http404
    time = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%fZ')
    time2 = make_aware(time, timezone=utc)
    items = models.ScheduleItem.objects.for_date(time2)
    _, urls = tools.download(items)
    if urls:
        urls.insert(0, static('dindon.mp3'))

    return JsonResponse(urls, safe=False)
