from django import forms
from django.forms import ModelForm
from .models import SqlScript
from .models import Run

class SqlScriptForm(ModelForm):
    class Meta:
        model = SqlScript
        fields = ["name", "description", "file"]

class RunForm(ModelForm):
    class Meta:
        model = Run
        fields = ["connstrings"]
