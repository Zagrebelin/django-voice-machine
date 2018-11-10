from datetime import datetime

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import Http404, JsonResponse
from django.utils.timezone import make_aware, utc, get_default_timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from . import models, tools


class DashView(TemplateView):
    template_name = 'dash.html'


@csrf_exempt
def mp3_filenames(request):
    timestr = request.POST.get('dt', None) or request.GET.get('dt', None) or None
    if not timestr:
        raise Http404
    dt = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%fZ')
    dt_utc = make_aware(dt, timezone=utc)
    dt_local = dt_utc.astimezone(get_default_timezone())
    items = models.ScheduleItem.objects.for_date(dt_local)
    _, urls = tools.download(items, dt_local)
    if urls:
        urls.insert(0, static('dindon.mp3'))

    return JsonResponse(urls, safe=False)
