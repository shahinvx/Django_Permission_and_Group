from django.urls import path, re_path
from django.urls.conf import include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('',Login.as_view(), name='login'),
    path('log_out/',Log_Out.as_view(), name='logout'),
    path('register/',Registration.as_view(), name='register'),
    path('home/',Home.as_view(), name='home'),
    path('permission/',Permission_User.as_view(),kwargs={'id': None}, name='permission'),
    path('permission/<id>/',Permission_User.as_view(), name='permission'),
    path('group_crt/',Group_Crt.as_view(), name='group_crt'),
    path('user_crtl/',User_Crtl.as_view(), name='user_crtl'),
    #url(r'^permission/(?P<id>\w+)/$', Permission_User.as_view(),name='permission'),
    #url(r'^permission/(?P<id>[0-9]+)/$', Permission_User.as_view(), name='permission'), 
    #re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    path('perm/',Permission_List.as_view(), name='User Perm'),
    path('user/',user_add.as_view(), name='User All'),
    path('profile_add/',Profile_Create.as_view(), name='Add'),
    path('types_add/',Types_Create.as_view(), name='Types Add'),
    path('user_add/',User_Create.as_view(), name='User Add'),
    path('group_add/',Group_Add.as_view(), name='Group Add'),
    path('group_upd/<pk>/',Group_pk_update.as_view(), name='User Update'),
]