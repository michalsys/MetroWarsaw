from django import forms
from django.core.exceptions import ValidationError

from metro_app.models import Character, Location


class NewCharacterForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(), label='Character name')

    class Meta:
        model = Character
        fields = ['name']
