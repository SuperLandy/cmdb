from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from assets.models import Asset, Administrator
import django.utils.timezone as timezone

# Create your views here.


@login_required()
def asset_asset(request, aid=None):
    """
    aid为None只显示部分资产信息，否则查询所有资产信息
    :param request:
    :param aid:
    :return:
    """
    if aid is None:
        assets_result = Asset.objects.all().values('id', 'ip', 'hostname', 'protocol')
        return render(request, 'assets/assets_asset.html', {'assets_result': assets_result})
    else:
        assets_result = {}
        result = Asset.objects.filter(id=aid).values()
        for row in result:
            assets_result = row
        return render(request, 'assets/assets_asset_info.html', {'assets_result': assets_result})


@login_required()
def asset_asset_delete(request, aid=None):
    role = request.session.get('is_superuser')
    if role:
        if request.method == 'GET':
            count = Asset.objects.filter(id=aid).count()
            if count == 0:
                return JsonResponse({'msg': '资产不存在'})
            else:
                Asset.objects.filter(id=aid).delete()
                return JsonResponse({'msg': '0000'})
        else:
            return JsonResponse({'msg': 'Method ERROR'})
    else:
        return JsonResponse({'msg': '权限不足'})


@login_required()
def asset_entry(request):
    """
    :param request:  get 获取资产用户信息，渲染表单，post录入资产
    :return:
    """
    if request.method == 'GET':
        user_obj = Administrator.objects.all().values('id', 'name')
        return render(request, 'assets/assets_asset_entry.html', {'user_obj': user_obj})
    if request.method == 'POST':
        ip = request.POST.get('ip', None)
        if ip is None:
            return JsonResponse({'msg': 'ip地址不能为空'})
        if Asset.objects.filter(ip=ip).count() != 0:
            return JsonResponse({'msg': 'ip地址已存在'})
        hostname = request.POST.get('hostname', None)
        if hostname is None:
            return JsonResponse({'msg': 'hostname不能为空'})
        public_ip = request.POST.get('public_ip', None)
        protocol = request.POST.get('protocol', None)
        if protocol is None:
            return JsonResponse({'msg': 'protocol不能为空'})
        port = request.POST.get('port', 22)
        assets_user_id = request.POST.get('assets_id', None)
        if assets_user_id is None:
            return JsonResponse({'msg': '资产用户不能为空'})
        vendor = request.POST.get('vendor', None)
        model = request.POST.get('model', None)
        cpu_cores = request.POST.get('cpu_cores', None)
        memory = request.POST.get('memory', None)
        disk_info = request.POST.get('disk_info', None)
        os = request.POST.get('os', None)
        sn = request.POST.get('sn', None)
        number = request.POST.get('number', None)
        remarks = request.POST.get('remarks', None)
        Asset.objects.create(ip=ip, hostname=hostname, public_ip=public_ip, protocol=protocol,  port=port,
                             assets_user_id=assets_user_id, vendor=vendor, model=model, cpu_cores=cpu_cores,
                             memory=memory, disk_info=disk_info, os=os, sn=sn, number=number, remarks=remarks
                             )
        return JsonResponse({'msg': '0000'})
    else:
        return redirect('/assets/asset/')


@login_required()
def asset_user(request, uid=None):
    """
    :param request:   get查询资产用户， post，判断用户权限，更新资产用户信息
    :param uid:
    :return:
    """
    role = request.session.get('is_superuser')
    if request.method == 'GET':
        if uid is None:
            user_result = Administrator.objects.all().values('id', 'name', 'date_created')
            return render(request, 'assets/assets_user.html', {'user_result': user_result})
        else:
            user_info = {}
            result = Administrator.objects.filter(id=uid).values()
            for row in result:
                user_info = row
            return render(request, 'assets/assets_user_info.html', {'user_info': user_info})
    if role:
        if request.method == 'POST':
            try:
                uid = request.POST.get('id')
                username = request.POST.get('username')
                password = request.POST.get('password')
                Administrator.objects.filter(id=uid).update(name=username, password=password,
                                                            date_updated=timezone.now())
                return JsonResponse({'msg': '0000'})
            except EOFError as err:
                return JsonResponse({'msg': err})
        else:
            return JsonResponse({'msg': '权限不足'})


@login_required()
def asset_user_entry(request):
    """
    权限判断，不是超级管理员不能录入资产用户
    :param request:
    :return:
    """
    role = request.session.get('is_superuser')
    if request.method == 'POST':
        if role:
            name = request.POST.get('username', None)
            if name is None:
                return JsonResponse({'msg': '资产用户名不能为空'})
            if Administrator.objects.filter(name=name).count() != 0:
                return JsonResponse({'msg': '资产用户名已存在'})
            password = request.POST.get('password', None)
            if password is None:
                return JsonResponse({'msg': '密码不能为空'})
            Administrator.objects.create(name=name, password=password)
            return JsonResponse({'msg': '0000'})
        else:
            return JsonResponse({'msg': '权限不足'})
    else:
        return render(request, 'assets/assets_user_entry.html')



@login_required()
def asset_user_delete(request, uid=None):
    """
    :param request:  判断权限删除资产用户
    :param uid:
    :return:
    """
    role = request.session.get('is_superuser')
    if role:
        if uid is None:
            return JsonResponse({'msg': 'Uid is None'})
        if request.method != 'POST':
            return JsonResponse({'msg': 'Method Error'})
        else:
            uid = request.POST.get('uid')
            Administrator.objects.filter(id=uid).delete()
            return JsonResponse({'msg': '0000'})
    else:
        return JsonResponse({'msg': '权限不足'})
