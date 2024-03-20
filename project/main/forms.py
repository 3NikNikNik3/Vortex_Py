from django import forms
from Format import Formats

TYPES = {'': 'Автоопределение'}
for i in Formats:
    TYPES.update({i.name: i.name})

class LoadFile(forms.Form):
    File = forms.FileField(label='1. Загрузите файл, который хотите редактировать')
    Type = forms.MultipleChoiceField(label='2. Выберите подходящий тип данных', widget=forms.RadioSelect, choices=TYPES)