from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from assets.models import Asset, Administrator, AssetGroup
import django.utils.timezone as timezone

# Create your views here.


@login_required()
def asset_asset(request, aid=None):
    """
    :param request:
    :param aid:
    :return:
    """
    if aid is None:
        return redirect('/assets/asset/group/')
    else:
        assets_result = {}
        result = Asset.objects.filter(id=aid).values()
        assets_name = Asset.objects.filter(id=aid).values('assets_user__name')[0]
        assets_group = Asset.objects.filter(id=aid).values('assets_group__group_name')[0]
        for row in result:
            assets_result = row
        return render(request, 'assets/assets_asset_info.html', {'assets_result': assets_result,
                                                                 'assets_name': assets_name,
                                                                 'assets_group': assets_group})


@login_required()
def asset_asset_group(request, gid=None):
    """
    gid为None显全部资产组名，否则查询具体组下的资产信息
    :param request:
    :param gid: 资产组ID
    :return:
    """
    if gid is None:
        list_group = AssetGroup.objects.all().values('group_id', 'group_name')
        return render(request, 'assets/assets_asset_group.html', {'list_group': list_group})
    else:
        list_assets = AssetGroup.objects.filter(group_id=gid).values('asset__id',  'asset__ip', 'asset__hostname',
                                                                     'asset__protocol')
        if list_assets[0].get('asset__id') is None:
            return redirect('/assets/asset/group/')
        else:
            return render(request, 'assets/assets_asset.html', {'list_assets': list_assets})


@login_required()
def asset_group(request, gid=None):
    """
    get： 查看资产组信息，group_id不为空，只查询单条信息
    :param request:
    :param gid:
    :return:
    """
    if request.method == 'GET':
        if gid is None:
            group_list = AssetGroup.objects.values().values('group_id', 'group_name')
            return render(request, 'assets/assets_group.html', {'group_list': group_list})
        else:
            group = AssetGroup.objects.filter(group_id=gid).values('group_id', 'group_name')
            return render(request, 'assets/assets_group_info.html', {'group': group})
    if request.method == 'POST':
        if gid is None:
            return JsonResponse({'msg': 'group_id不为空'})
        group_name = request.POST.get('group_name', None)
        if group_name is None:
            return JsonResponse({'msg': '资产组名不为空'})
        AssetGroup.objects.filter(group_id=gid).update(group_name=group_name)
        return JsonResponse({'msg': '更新成功'})


@login_required()
def asset_group_create(request):
    """
    post 创建资产组
    :param request:
    :return:
    """
    role = request.session.get('is_superuser')
    if request.method == 'POST':
        if role:
            group_name = request.POST.get('group_name', None)
            if group_name is None:
                return JsonResponse({'msg': '组名不为空'})
            if AssetGroup.objects.filter(group_name=group_name).count() != 0:
                return JsonResponse({'msg': '组名已存在'})
            AssetGroup.objects.create(group_name=group_name)
            return JsonResponse({'msg': '资产组添加成功'})
        else:
            return JsonResponse({'msg': '权限不足'})
    else:
        return render(request, 'assets/assets_group_create.html')


@login_required()
def asset_group_delete(request):
    role = request.session.get('is_superuser')
    if request.method == 'POST':
        if role:
            group_id = request.POST.get('group_id')
            if AssetGroup.objects.filter(group_id=group_id).count() == 0:
                return JsonResponse({'msg': '资产组不存在'})
            AssetGroup.objects.filter(group_id=group_id).delete()
            return JsonResponse({'msg': '删除成功'})
        else:
            return JsonResponse({'msg': '权限不足'})
    else:
        return redirect('/assets/group/')


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
        group_obj = AssetGroup.objects.all().values('group_id', 'group_name')
        return render(request, 'assets/assets_asset_entry.html', {'user_obj': user_obj, 'group_obj': group_obj})
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
        assets_group_id = request.POST.get('group_id', None)
        if assets_group_id is None:
            return JsonResponse({'msg': '资产组不能为空'})
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
                             assets_user_id=assets_user_id, assets_group_id=assets_group_id, vendor=vendor, model=model,
                             cpu_cores=cpu_cores, memory=memory, disk_info=disk_info, os=os, sn=sn, number=number,
                             remarks=remarks
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
