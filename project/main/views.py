"""views main"""

import os.path
from random import randint as rand

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from main.models import User
from main.forms import LoadFile
from format import get, load_from_file, Formats, Types
from file_type import Istream


# Create your views here.
def random_key() -> str:
    """get random key"""

    arr = '1234567890qwertyuiopasdfghjklzxcvbnm'
    ans = ''
    for i in range(500):
        ans += arr[rand(0, len(arr) - 1)]
    return ans


def get_random_key() -> str:
    """get random key one"""

    key = random_key()
    while len(User.objects.filter(key=key)) != 0:
        key = random_key()
    user = User(key=key)
    user.save()
    return key


def load(req):
    """main load"""

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
        if not form.is_valid() and 'Type' in form.data and 'File' in req.FILES:
            user = User.objects.filter(key=key)
            if len(user) != 1:
                user = User(key=key)
                user.save()
            else:
                user = user[0]

            if form.data['Type'] != '':
                f = get(form.data['Type'])
            else:
                f = get('.' + str(req.FILES['File']).rsplit('.', maxsplit=1)[-1])

            if req.FILES['File'].size > f.max_size != -1:
                return render(req, 'load.html', {'form': LoadFile(), 'error': True}, status=413)

            data = bytes()
            for i in req.FILES['File'].chunks():
                data += i

            file = f.fun_from(data)
            file.save('data/' + str(user.id), f.type_file)
            return HttpResponseRedirect('/edit')
        con['form'] = form
    else:
        con['form'] = LoadFile()
        con['error'] = False

    return render(req, 'load.html', con)


def new(req):
    """main create new file"""

    arr = []
    for i in Types:
        arr.append({
            'name': Types[i].name,
            'id': i,
            'dop_op': Types[i].new_file.get_html_option()
        })
    con = {'types': arr}

    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        ans = render(req, 'new_file.html')
        ans.set_signed_cookie('key_user', get_random_key())
        return ans
    if len(User.objects.filter(key=key)) == 0:
        user = User(key=key)
        user.save()

    if req.method == 'POST':
        if 'type' in req.POST:
            if req.POST['type'] in Types:
                file = Types[req.POST['type']].new_file.fun(req.POST)
                file.save(f'data/{User.objects.filter(key=key)[0].id}', req.POST['type'])
                return HttpResponseRedirect('/edit')

    return render(req, 'new_file.html', con)


def save(req):
    """main save file"""

    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        return HttpResponseRedirect('/load')

    user = User.objects.filter(key=key)
    if len(user) != 1:
        return HttpResponseRedirect('/load')
    user = user[0]

    del_ = False
    if os.path.exists('data/' + str(user.id) + 'save'):
        type_file, file = load_from_file('data/' + str(user.id))
        del_ = True
    else:
        if not os.path.exists('data/' + str(user.id)):
            return HttpResponseRedirect('/load')

        type_file, file = load_from_file('data/' + str(user.id))
    if req.method == 'POST':
        if 'type' in req.POST and 'name' in req.POST:
            f = get(req.POST['type'])
            res = HttpResponse(f.fun_to(file), content_type='application/octet-stream')
            res['Content-Type'] = 'charset=utf-16'
            res['Content-Disposition'] = ('attachment; filename=' + req.POST['name'] +
                                          (f.ext if ('add_ras' in req.POST) else ''))
            if del_:
                os.remove('data/' + str(user.id) + 'save')
            return res

    arr = []
    for i in Formats:
        if i.type_file == type_file:
            arr.append(i.name)

    return render(req, 'save.html', {'types': arr})


def edit(req):
    """main edit file"""

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
            file.next(3)
            type_file = file.get_str(1)
            file = Types[type_file].load_fun_edit(req.POST)
            file.save('data/' + str(user.id), type_file)
        else:
            type_file, file = load_from_file('data/' + str(user.id))
    else:
        type_file, file = load_from_file('data/' + str(user.id))

    return Types[type_file].fun_edit(req, file)


def transform(req):
    """main transform file"""

    key = req.get_signed_cookie('key_user', default='')
    if key == '':
        return HttpResponseRedirect('/load')

    user = User.objects.filter(key=key)
    if len(user) != 1:
        return HttpResponseRedirect('/load')
    user = user[0]

    if not os.path.exists('data/' + str(user.id)):
        return HttpResponseRedirect('/load')

    type_file, file = load_from_file('data/' + str(user.id))

    if req.method == 'POST':
        if 'go' in req.POST and 'why' in req.POST:
            t = Types[type_file].get_trans(req.POST['why'])
            if t is not None:
                t.fun_main(file, req.POST).save('data/' + str(user.id), req.POST['why'])
                type_file, file = load_from_file('data/' + str(user.id))
        elif 'save' in req.POST and 'why' in req.POST:
            t = Types[type_file].get_trans(req.POST['why'])
            if t is not None:
                t.fun_main(file, req.POST).save('data/' + str(user.id) + 'save', req.POST['why'])
                return HttpResponseRedirect('/save')

    arr = []
    for i in Types[type_file].transform:
        if i.fun_can(file):
            arr.append({'where': i.where, 'html': i.get_html_option(), 'name': Types[i.where].name})

    return render(req, 'transform.html', {'types': arr, 'from': Types[type_file].name,
                                          'ok': len(arr) > 0})


def index(req):
    """main index"""

    return render(req, 'index.html')
