from django import forms
from Format import ARRAY

TYPES = {'': 'Автоопределение'}
for i in ARRAY:
    TYPES.update({i: i})

class LoadFile(forms.Form):
    File = forms.FileField(label='Файл')
    Type = forms.MultipleChoiceField(label='Как открывать', widget=forms.RadioSelect, choices=TYPES)