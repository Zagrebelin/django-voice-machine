import json

from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from . import models


class DashView(TemplateView):
    template_name = 'dash.html'



class Mp3Filenames(ListView):
    model = models.RenderedScheduleItem

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        timestr = self.kwargs.get('dt')
        time = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%fZ')
        time2 = make_aware(time)
        return qs.filter(when=time2).order_by('order')

    def render_to_response(self, context, **response_kwargs):
        os = context['object_list']
        lst = [i.file.url for i in os]
        return HttpResponse(json.dumps(lst))

    def post(self, request, *args, **kwargs):
        self.kwargs = json.loads(request.body.decode('utf-8'))
        return self.get(request, *args, **kwargs)