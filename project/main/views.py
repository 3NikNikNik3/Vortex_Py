import os.path

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from random import randint as rand
from main.models import User
from datetime import datetime
from main.forms import LoadFile
from Format import Get, LoadFromFile, Formats, FunEdit, LoadFunEdit
from FileType import Istream


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
        ans = render(req, 'load.html', {'form': LoadFile()})
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
                user = User(key=key, data_create=datetime.now())
                user.save()
            else:
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
            return HttpResponseRedirect('/edit')
        con['form'] = form
    else:
        con['form'] = LoadFile()

    return render(req, 'load.html', con)


def Save(req):
    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        return HttpResponseRedirect('/load')

    user = User.objects.filter(key=key)
    if len(user) != 1:
        return HttpResponseRedirect('/load')
    user = user[0]

    if not os.path.exists('data/' + str(user.id)):
        return HttpResponseRedirect('/load')

    type, file = LoadFromFile('data/' + str(user.id))
    if 'type' in req.GET and 'name' in req.GET:
        res = HttpResponse(Get(req.GET['type']).funTo(file), content_type='text/txt')
        res['Content-Disposition'] = 'attachment; filename=' + req.GET['name']
        return res

    arr = []
    for i in Formats:
        if i.type == type:
            arr.append(i.name)

    return render(req, 'save.html', {'types': arr})


def Edit(req):
    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        return HttpResponseRedirect('/load')

    user = User.objects.filter(key=key)
    if len(user) != 1:
        return HttpResponseRedirect('/load')
    user = user[0]

    if not os.path.exists('data/' + str(user.id)):
        return HttpResponseRedirect('/load')

    if req.method == 'POST':
        file = Istream('data/' + str(user.id))
        file.Next(3)
        type = file.GetInt(2)
        LoadFunEdit[type](req.POST).Save('data/' + str(user.id), type)

    type, file = LoadFromFile('data/' + str(user.id))
    return FunEdit[type](req, file)
