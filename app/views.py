from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from assets.models import Asset, Administrator, AssetGroup

# Create your views here.


def index(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth = authenticate(username=username, password=password)
        if auth is None:
            return render(request, 'index.html', {'result': '密码错误'})
        elif auth.is_active is False:
            return render(request, 'index.html', {'result': '用户已禁用'})
        else:
            login(request, user=auth)
            request.session['is_superuser'] = auth.is_superuser
            request.session['username'] = auth.username
            return redirect('/dashboard/')
    else:
        return redirect('/')


@login_required()
def dashboard(request):

    user_info = {}
    list_group = []
    users = User.objects.all().count()
    assets_group = AssetGroup.objects.all().count()
    assets_total = Asset.objects.all().count()
    assets_user = Administrator.objects.all().count()
    user_info['users'] = users
    user_info['assets_group'] = assets_group
    user_info['assets_total'] = assets_total
    user_info['assets_user'] = assets_user
    group_name = AssetGroup.objects.all().values('group_id', 'group_name')
    for group_id in group_name:
        result = Asset.objects.filter(assets_group_id=group_id['group_id']).count()
        list_group.append((group_id['group_name'], result))
    return render(request, 'dashboard.html', {"user_info": user_info,
                                              'list_group': list_group})


@login_required()
def user_logout(request):
    logout(request)
    return redirect('/')
