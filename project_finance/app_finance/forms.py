from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings
from django import forms
import datetime
import pandas as pd

widgets_textinput = forms.TextInput(
    attrs={
        "class": "form-control",
    }
)


# スクレイピングフォーム
class TextForm(forms.Form):

    today=datetime.datetime.today()
    code = forms.CharField(label="証券コード", widget=widgets_textinput)
    start = forms.DateField(label="開始日",initial=(pd.Period(today, 'D') - 365).start_time)
    end = forms.DateField(label="終わり日",initial=today)