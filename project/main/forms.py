from django import forms
from format import Formats

TYPES = {'': 'Автоопределение'}
for i in Formats:
    TYPES.update({i.name: f'{i.name} ({i.max_size / 1024}Кб)' if i.max_size != -1 else i.name})

'''class FileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.max_size = kwargs.pop('max_size', -1)

        super(FileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(FileField, self).clean(*args, **kwargs)
        file = data.file
        if self.max_size != -1:
            try:
                if file.size > self.max_size:
                    raise forms.ValidationError((f'Максимальный размер файла: {self.max_size / 1024} Кб, а Вы загрузили {file.size / 1024} Кб'))
            except AttributeError:
                pass
        return data
'''

class LoadFile(forms.Form):
    File = forms.FileField(label='1. Загрузите файл, который хотите редактировать')
    Type = forms.MultipleChoiceField(label='2. Выберите подходящий тип данных', widget=forms.RadioSelect, choices=TYPES)