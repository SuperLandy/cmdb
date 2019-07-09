from django.shortcuts import render
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import re
# Create your views here.


@login_required()
def user(request, uid=None):
    """
    :param request:  请求体
    :param uid:    如果uid是 None，则查询所有用户信息，否则只查询uid用户
    :return: render
    """

    if uid is None:
        user_data = User.objects.all().values('id', 'is_superuser', 'is_active', 'username', 'email')
        return render(request, 'users/user.html', {'user_data': user_data})
    else:
        user_result = User.objects.filter(id=uid).values('id', 'is_superuser', 'is_active', 'username', 'email')
        return render(request, 'users/users_user.html', {'user_result': user_result})


@login_required()
def delete(request, uid):
    """
    :param request: 判断用户权限，不是超级管理员不允许删除
    :param uid:  必须携带被删除用户id
    :return:
    """
    role = request.session.get('is_superuser')
    if role:
        if uid is not None:
            User.objects.filter(id=uid).delete()
            return JsonResponse({'msg': '0000'})
        else:
            return JsonResponse({'msg': '用户ID为空'})
    else:
        return JsonResponse({'msg': '权限不足'})


@login_required()
def update(request, uid):
    """
    :param request:   权限判断
    :param uid:
    :return:
    """
    role = request.session.get('is_superuser')
    if request.method == 'POST':
        if role:
            username = request.POST.get('username')
            power = request.POST.get('power')
            email = request.POST.get('email')
            _t = User.objects.get(id=uid)
            _t.username = username
            _t.is_superuser = power
            _t.email = email
            _t.save()
            return JsonResponse({'msg': '0000'})
        else:
            return JsonResponse({'msg': '权限不足'})
    else:
        return JsonResponse({'msg': '请求错误'})


@login_required()
def add(request):
    """
    :param request:  权限判断，是超管允许删除用户信息，POST请求
    :return:
    """
    role = request.session.get('is_superuser')

    if request.method == 'GET':
        return render(request, 'users/users_user_add.html')
    elif request.method == 'POST':
        if role:
            email = request.POST.get('email', None)
            if email is None:
                return JsonResponse({'msg': 'email地址为空'})
            else:
                if re.match(r"^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$", email) is None:
                    return JsonResponse({'msg': 'email地址不合法'})
            username = request.POST.get('username', None)
            role = request.POST.get('role', None)
            password = request.POST.get('password', None)
            user_count = User.objects.filter(username=username).count()
            email_count = User.objects.filter(email=email).count()
            if user_count != 0:
                return JsonResponse({'msg': '用户已存在'})
            if email_count != 0:
                return JsonResponse({'msg': '邮箱已存在'})
            if username is not None and role is not None and password is not None:
                if role == '1':
                    User.objects.create(username=username, password=make_password(password), is_superuser=True,
                                        email=email)
                    return JsonResponse({'msg': '0000'})
                else:
                    User.objects.create(username=username, password=make_password(password), is_superuser=False,
                                        email=email)
                    return JsonResponse({'msg': '0000'})
        else:
            return JsonResponse({'msg': '权限不足'})
    else:
        return JsonResponse({'msg': '系统错误'})
