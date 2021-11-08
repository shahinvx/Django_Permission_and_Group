from django.http import HttpResponse, JsonResponse
from django.core import serializers
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db.models.expressions import Value
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import fields, generics, serializers
from rest_framework import status
from django.contrib.auth.models import User, Group, Permission

from .serializers import *
from .serializers import Profile_Details_Serializers, Profile_Type_Serializer, My_User_Serializer, Group_Serializer, PermissionList_Serializer, User_Serializer
from .models import *
# Create your views here.
from .models_forms import User_Register_Form, User_Login_Form, Group_Form, DynamicForm
from django.contrib import messages
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authtoken.models import Token

# Decorators
from common_utils.decorators import if_log_then_go, my_permission_chk
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth import authenticate, login, logout


class Login(APIView):
    @method_decorator(if_log_then_go, name='dispatch')
    def get(self, request, format=None):
        # return Response({'Text' : 'Home Page'})
        form = User_Login_Form()
        context = {'Text': 'Please Login', 'form': form}
        return render(request, 'login.html', context)

    def post(self, request,):
        form = User_Login_Form(request.POST)
        user_name = request.POST.get('username')
        user_pass = request.POST.get('password')
        try:
            my_user = User.objects.get(username=user_name)
        except:
            my_user = 0
        if my_user:
            my_user = authenticate(username=user_name, password=user_pass)
            if my_user:
                try:
                    my_user.auth_token.delete()
                except:
                    a = 0
                request.session['user'] = user_name
                user_token = Token.objects.create(user=my_user)
                login(request, my_user)
                messages.success(
                    request, f'Hello !! Welcome again {request.user}')
                return redirect('home')
            else:
                form = User_Login_Form()
                context = {'Text': 'Wrong Password', 'form': form}
                return render(request, 'login.html', context)
        else:
            form = User_Login_Form()
            context = {'Text': 'No User', 'form': form}
            return render(request, 'login.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Log_Out(APIView):
    def get(self, request, format=None):
        del request.session['user']
        request.user.auth_token.delete()
        logout(request)

        return redirect('login')

class Registration(APIView):
    def post(self, request,):
        form = User_Register_Form(request.POST)
        if form.is_valid():
            user = My_User(
                email=form['email'].value(),
                username=form['username'].value()
            )
            user.set_password(form['password'].value())
            user.full_name = form['full_name'].value()
            user.age = form['age'].value()
            user.address = form['address'].value()
            user.save()
            Token.objects.create(user=user)
            user_name = form.cleaned_data.get('username')
            messages.success(request, f'Account is created for {user_name}')
            return redirect('login')
        else:
            print(form)
            form = User_Register_Form()

        return render(request, 'register_form.html', {'form': form})

    @method_decorator(if_log_then_go, name='dispatch')
    def get(self, requset, format=None):
        form = User_Register_Form()
        return render(requset, 'register_form.html', {'form': form})

class Home(APIView):
    @method_decorator(login_required(login_url='login'), name='dispatch')
    def get(self, requset, format=None):

        context = {'Text': 'Please Login FIrst'}
        return render(requset, 'home.html', context)

from django.http import JsonResponse
from django.core import serializers
class User_Crtl(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_control.html'
    serializer_class = Group_Serializer

    def get(self, request, format=None):
        data = My_User_Table(My_User.objects.all(), many=True).data
        user_data = []
        for i in data:
            user_data.append(dict(i))

        GroupInfo = Group_Serializer(Group.objects.all(), many=True).data


        context = {'Text': 'User Control','valid':True,'Group': GroupInfo, 'Data':user_data,'Column':list(user_data[0].keys())}
        #if request.is_ajax():
        if request.GET.get('Do') == 'get_info':
            user_id = request.GET.get("user_id", None)
            my_user = My_User.objects.get(pk=user_id)
            my_user_group = my_user.groups.all()
            my_user = My_User_Table(my_user, many=False).data
            user_group = []
            for i in my_user_group:
                user_group.append(str(i))
            ajax_data ={'Group': GroupInfo, 'valid':True, 'user_group': user_group, 'user_info':my_user}
            return JsonResponse(ajax_data, status=200)

        if request.GET.get('Do') == 'get_del':
            user_id = request.GET.get("user_id", None)
            my_user = My_User.objects.get(pk=user_id)
            my_user = My_User_Table(my_user, many=False).data

            ajax_data ={'valid':True, 'user_info':my_user}
            return JsonResponse(ajax_data, status=200)

        return Response(context)

    def post(self, request, format=None):

        flag = False
        if request.POST.get('Do') != 'add_user' and request.POST.get('Do') != 'del_user':
            my_user = My_User.objects.get(pk=request.POST.get('user_id_m'))
            my_user.email = request.POST.get('email_m')
            my_user.full_name = request.POST.get('full_name_m')
            if request.POST.get('age_m') == '': my_user.age = 0
            else : my_user.age = request.POST.get('age_m')
            my_user.address = request.POST.get('address_m')

            if request.POST.get('dropdown') != 'none':
                my_group = Group.objects.get(pk=request.POST.get('dropdown'))
                my_user.groups.clear()
                my_group.user_set.add(my_user)
                print('User instence : ',my_user)
            my_user.save()

            data = My_User_Table(My_User.objects.all(), many=True).data

            user_data = []
            for i in data:
                user_data.append(dict(i))

            GroupInfo = Group_Serializer(Group.objects.all(), many=True).data

            context = {'Text': 'User Control','valid':flag,'Group': GroupInfo, 'Data':user_data,'Column':list(user_data[0].keys())}

            return Response(context)
        

        elif request.POST.get('Do') == 'add_user':
            try:
                my_user = My_User.objects.create_user(username=request.POST.get('user_name'),email=request.POST.get('user_email'))
                #my_user.first_name = value['NAME']
                my_user.set_password(request.POST.get('user_pass'))
                my_user.save()
                Token.objects.create(user=my_user)
                flag = True
            except:
                flag = False
        
        elif request.POST.get('Do') == 'del_user':
            try:
                user_sec_key = My_Sec_Key(Secret_Key.objects.get(s_key=request.POST.get("sec_key"))).data
                if user_sec_key['s_name'] == 'user_del_key':
                    user_id = request.POST.get("user_id", None)
                    my_user = User.objects.get(pk=user_id)
                    my_user.delete()

                    flag = True
                else:                        
                    flag=False
                    context = {'valid':flag}
                    return JsonResponse(context, status=200)
            except:
                flag=False
                context = {'valid':flag}
                return JsonResponse(context, status=200)

        data = My_User_Table(My_User.objects.all(), many=True).data

        user_data = []
        for i in data:
            user_data.append(dict(i))

        GroupInfo = Group_Serializer(Group.objects.all(), many=True).data

        context = {'Text': 'User Control','valid':flag,'Group': GroupInfo, 'Data':user_data,'Column':list(user_data[0].keys())}
        
        return JsonResponse(context, status=200)

class Group_Crt(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'group.html'
    serializer_class = Group_Serializer

    def get(self, request):
        qry = Group.objects.all()
        data = Group_Serializer(qry, many=True).data
        GroupInfo = []
        for key in data:
            GroupInfo.append(dict(key))
        context = {'Text': 'Create Group', 'Group': GroupInfo}
        return Response(context)

    def post(self, request, *args, **kwargs):
        grp_id = request.POST.getlist('dropdown')
        btn_t = request.POST.getlist('link_a')

        name = request.POST.getlist('group_name')
        name = name[0]
        if name and btn_t[0] == 'crt':
            try:
                new_grp = Group(name=name)
                new_grp.save()
            except:
                messages.success(
                    request, f'Group is Already exist by this name : {name}')

        name = request.POST.getlist('group_name_upd')
        if name[0] not in (None, '') and btn_t[0] == 'upd':
            grp_upd = Group.objects.get(id=grp_id[0])
            grp_upd.name = name[0]
            grp_upd.save()

        if btn_t[0] == 'del':
            grp_upd = Group.objects.get(id=grp_id[0])
            grp_upd.delete()

        qry = Group.objects.all()
        data = Group_Serializer(qry, many=True).data
        GroupInfo = []
        for key in data:
            GroupInfo.append(dict(key))

        context = {'Text': 'Create Group', 'Group': GroupInfo}
        return Response(context)

    def put(self, request, *args, **kwargs):
        name_1 = request.PUT.getlist('dropdown')

class Permission_User(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'permission.html'
    serializer_class = Group_Serializer

    @method_decorator(login_required(login_url='login'), name='dispatch')
    def get(self, request, format=None, *args, **kwargs):

        snippets = Group.objects.all()
        serializer = Group_Serializer(snippets, many=True).data
        data_dict = []
        GroupInfo = []
        for dat in serializer:
            data_dict.append(dict(dat))
            if str(dict(dat)['id']) == kwargs['id']:
                GroupInfo = dict(dat)

        people_2 = Permission.objects.all().values("id", "name")
        people_2 = list(people_2)
        context = {'Text': 'Give Your pemission', 'Data': people_2,
                   'Group': data_dict, 'GroupInfo': GroupInfo}  # , 'GroupPerm':permission
        return Response(context)
        # return render(requset, 'permission.html', context)

    def post(self, request, *args, **kwargs):

        snippets = Group.objects.all()
        serializer = Group_Serializer(snippets, many=True).data
        data_dict = []
        GroupInfo = []
        for dat in serializer:
            data_dict.append(dict(dat))
            if str(dict(dat)['id']) == kwargs['id']:
                GroupInfo = dict(dat)

        GroupInfo['permissions'] = list(
            map(int, request.POST.getlist('permissions')))
        grp_update = Group.objects.get(id=kwargs['id'])

        grp_update.permissions.clear()

        for num in GroupInfo['permissions']:
            grp_update.permissions.add(num)

        people_2 = list(Permission.objects.all().values("id", "name"))
        context = {'Text': 'Give Your pemission', 'Data': people_2,
                   'Group': data_dict, 'GroupInfo': GroupInfo}  # , 'GroupPerm':permission
        return Response(context)


class Profile_Create(generics.CreateAPIView):
    # authentication_classes = ()                                    # if REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES'} is added
    #permission_classes = ()
    serializer_class = Profile_Details_Serializers


class Types_Create(generics.ListCreateAPIView):
    # authentication_classes = ()                                    # if REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES'} is added
    #permission_classes = ()
    serializer_class = Profile_Type_Serializer

    def get_queryset(self):
        return ProfileType.objects.all()


class User_Create(generics.CreateAPIView):
    #authentication_classes = ()
    #permission_classes = ()
    serializer_class = My_User_Serializer


# auth_permission http://127.0.0.1:8000/prmt/permission_all/
class Permission_List(generics.ListAPIView):
    queryset = Permission.objects.all()[:10]
    serializer_class = PermissionList_Serializer


class Group_Add(generics.CreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'permission.html'
    serializer_class = Group_Serializer


class Group_Update(generics.UpdateAPIView):
    serializer_class = Group_Serializer


# [GET,PUT, PATCH] with <pk> set url/<pk>
class Group_pk_update(generics.RetrieveUpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = Group_Serializer


# http://127.0.0.1:8000/prmt/user_add/
class user_add(generics.CreateAPIView):
    serializer_class = User_Serializer
