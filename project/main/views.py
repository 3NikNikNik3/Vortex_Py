from django.shortcuts import render
from random import randint as rand
from main.models import User
from datetime import datetime
from main.forms import LoadFile
from Format import Get, LoadFromFile

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
            user = User.objects.filter(key=key)
            if len(user) != 1:
                return 'error'
            user = user[0]
            if form.data['Type'] != '':
                f = Get(form.data['Type'])
            else:
                f = Get('.' + str(req.FILES['File']).split('.')[-1])
            data = bytes()
            for i in req.FILES['File'].chunks():
                data += i
            file = f.funFrom(data)
            file.Save('data/' + str(user.id), f.type)
        con['form'] = form
    else:
        con['form'] = LoadFile()

    return render(req, 'load.html', con)
