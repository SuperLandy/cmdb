"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from assets import views

urlpatterns = [
    # path('asset/', views.asset_asset),
    path('asset/group/', views.asset_asset_group),
    path('asset/group/<uuid:gid>/', views.asset_asset_group),

    path('asset/<uuid:aid>/', views.asset_asset),
    path('asset/<uuid:aid>/delete/', views.asset_asset_delete),

    path('group/', views.asset_group),
    path('group/<uuid:gid>/', views.asset_group),
    path('group/create/', views.asset_group_create),
    path('group/delete/', views.asset_group_delete),

    path('user/', views.asset_user),
    path('user/entry/', views.asset_user_entry),
    path('user/<uuid:uid>/', views.asset_user),
    path('user/<uuid:uid>/delete/', views.asset_user_delete),
    path('entry/', views.asset_entry),
]
