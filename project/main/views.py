from django.shortcuts import render
from random import randint as rand
from main.models import User
from datetime import datetime
from main.forms import LoadFile
from Format import Get

# Create your views here.
def random_key() -> str:
    arr = '1234567890qwertyuiopasdfghjklzxcvbnm'
    ans = ''
    for i in range(500):
        ans += arr[rand(0, len(arr) - 1)]
    return ans

def Load(req):
    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        ans = render(req, 'load.html', {'form': LoadFile() })
        key = random_key()
        while len(User.objects.filter(key=key)) != 0:
            key = random_key()
        ans.set_signed_cookie('key_user', key)
        user = User(key=key, date_create=datetime.now())
        user.save()
        return ans

    con = {}
    if req.method == 'POST':
        form = LoadFile(req.POST, req.FILES)
        if not form.is_valid():
            #! Загрузка
            pass
            #type = Get(form.Type)
            #print(req.FILES['File'])
        con['form'] = form
    else:
        con['form'] = LoadFile()

    return render(req, 'load.html', con)
