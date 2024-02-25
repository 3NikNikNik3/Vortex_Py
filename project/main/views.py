import os.path

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from random import randint as rand
from main.models import User
from datetime import datetime
from main.forms import LoadFile
from Format import Get, LoadFromFile, Formats, Types
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

    del_ = False
    if os.path.exists('data/' + str(user.id) + 'save'):
        type, file = LoadFromFile('data/' + str(user.id))
        del_ = True
    else:
        if not os.path.exists('data/' + str(user.id)):
            return HttpResponseRedirect('/load')

        type, file = LoadFromFile('data/' + str(user.id))
    if req.method == 'POST':
        if 'type' in req.POST and 'name' in req.POST:
            f = Get(req.POST['type'])
            res = HttpResponse(f.funTo(file), content_type='text/txt')
            res['Content-Disposition'] = ('attachment; filename=' + req.POST['name'] +
                                          (f.ext if ('add_ras' in req.POST) else ''))
            if del_: os.remove('data/' + str(user.id) + 'save')
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
        if 'save' in req.POST:
            file = Istream('data/' + str(user.id))
            file.Next(3)
            type = file.GetStr(1)
            file = Types[type].LoadFunEdit(req.POST)
            file.Save('data/' + str(user.id), type)
        else:
            type, file = LoadFromFile('data/' + str(user.id))
    else:
        type, file = LoadFromFile('data/' + str(user.id))

    return Types[type].FunEdit(req, file)


def Transform(req):
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

    if req.method == 'POST':
        if 'go' in req.POST and 'why' in req.POST:
            t = Types[type].GetTrans(req.POST['why'])
            if not t is None:
                t.funMain(file, req.POST).Save('data/' + str(user.id), req.POST['why'])
                return HttpResponse(status=204)
        elif 'save' in req.POST and 'why' in req.POST:
            t = Types[type].GetTrans(req.POST['why'])
            if not t is None:
                t.funMain(file, req.POST).Save('data/' + str(user.id) + 'save', req.POST['why'])
                return HttpResponseRedirect('/save')

    arr = []
    for i in Types[type].transform:
        if i.funCan(file):
            arr.append({'where': i.where, 'html': i.GetHrmlOption(), 'name': Types[i.where].name})

    return render(req, 'transform.html', {'types': arr, 'from': Types[type].name})
