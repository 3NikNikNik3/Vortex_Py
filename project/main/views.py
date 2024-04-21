import os.path

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from random import randint as rand
from main.models import User
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

def get_random_key() -> str:
    key = random_key()
    while len(User.objects.filter(key=key)) != 0:
        key = random_key()
    user = User(key=key)
    user.save()
    return key


def Load(req):
    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        ans = render(req, 'load.html', {'form': LoadFile(), 'error': False})
        ans.set_signed_cookie('key_user', get_random_key())
        return ans
    if len(User.objects.filter(key=key)) == 0:
        user = User(key=key)
        user.save()

    con = {}
    if req.method == 'POST':
        form = LoadFile(req.POST, req.FILES)
        if not form.is_valid():
            user = User.objects.filter(key=key)
            if len(user) != 1:
                user = User(key=key)
                user.save()
            else:
                user = user[0]

            if form.data['Type'] != '':
                f = Get(form.data['Type'])
            else:
                f = Get('.' + str(req.FILES['File']).split('.')[-1])

            if req.FILES['File'].size > f.max_size and f.max_size != -1:
                return render(req, 'load.html', {'form': LoadFile(), 'error': True}, status=413)

            data = bytes()
            for i in req.FILES['File'].chunks():
                data += i

            file = f.funFrom(data)
            file.Save('data/' + str(user.id), f.type)
            return HttpResponseRedirect('/edit')
        con['form'] = form
    else:
        con['form'] = LoadFile()
        con['error'] = False

    return render(req, 'load.html', con)


def New(req):
    arr = []
    for i in Types:
        arr.append({
            'name': Types[i].name,
            'id': i,
            'dop_op': Types[i].new_file.GetHtmlOption()
        })
    con = {'types': arr}

    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        ans = render(req, 'new_file.html')
        ans.set_signed_cookie('key_user', get_random_key(), con)
        return ans
    if len(User.objects.filter(key=key)) == 0:
        user = User(key=key)
        user.save()

    if req.method == 'POST':
        if 'type' in req.POST:
            if req.POST['type'] in Types:
                file = Types[req.POST['type']].new_file.fun(req.POST)
                file.Save(f'data/{User.objects.filter(key=key)[0].id}', req.POST['type'])
                return HttpResponseRedirect('/edit')

    return render(req, 'new_file.html', con)


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
            print(req.POST['name'])
            f = Get(req.POST['type'])
            res = HttpResponse(f.funTo(file), content_type='application/octet-stream')
            res['Content-Type'] = 'charset=utf-16'
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
                type, file = LoadFromFile('data/' + str(user.id))
        elif 'save' in req.POST and 'why' in req.POST:
            t = Types[type].GetTrans(req.POST['why'])
            if not t is None:
                t.funMain(file, req.POST).Save('data/' + str(user.id) + 'save', req.POST['why'])
                return HttpResponseRedirect('/save')

    arr = []
    for i in Types[type].transform:
        if i.funCan(file):
            arr.append({'where': i.where, 'html': i.GetHtmlOption(), 'name': Types[i.where].name})

    return render(req, 'transform.html', {'types': arr, 'from': Types[type].name, 'ok': len(arr) > 0})


def Index(req):
    return render(req, 'index.html')