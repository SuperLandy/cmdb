from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from assets.models import Asset, Administrator
from datetime import datetime

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
    uid = request.session.get('_auth_user_id')
    user_info = {}
    user_data = list(User.objects.filter(id=uid).values('is_superuser', 'username'))[0]
    users = User.objects.all().count()
    user_online = Session.objects.filter(expire_date__gte=datetime.now()).count()
    assets_total = Asset.objects.all().count()
    assets_user = Administrator.objects.all().count()
    user_info['user_data'] = user_data
    user_info['users'] = users
    user_info['user_online'] = user_online
    user_info['assets_total'] = assets_total
    user_info['assets_user'] = assets_user
    return render(request, 'dashboard.html', {"user_info": user_info})


@login_required()
def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_search = User.objects.filter(username=username).count()
        email_search = User.objects.filter(email=email).count()
        if user_search != 0:
            return render(request, 'register.html', {'result': '用户已存在!'})
        elif email_search != 0:
            return render(request, 'register.html', {'result': '邮箱已存在!'})
        else:
            User.objects.create_user(username=username, email=email, password=password)
            return render(request, 'register.html', {'result': '成功'})
    else:
        return redirect('/')
