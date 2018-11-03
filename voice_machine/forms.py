from django import forms
from django.contrib.admin.widgets import AdminTimeWidget

from . import models


class ScheduleItemForm(forms.ModelForm):
    class Meta:
        model = models.ScheduleItem
        exclude = []
        widgets = {'voice_type': forms.RadioSelect,
                   'voice_emotion': forms.RadioSelect,
                   'time': AdminTimeWidget}

