from django import forms
from Format import Formats

TYPES = {'': 'Автоопределение'}
for i in Formats:
    TYPES.update({i.name: i.name})

class LoadFile(forms.Form):
    File = forms.FileField(label='Файл')
    Type = forms.MultipleChoiceField(label='Как открывать', widget=forms.RadioSelect, choices=TYPES)