from django.forms import ModelForm
from django import forms
from django.forms.forms import Form
from .models import ProfileDetails, My_User
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token

class User_Register_Form(ModelForm):
    class Meta:
        model = My_User
        fields = ['username', 'email', 'password', 'full_name', 'age', 'address']
        extra_kwargs = {'password': {'write_only': True}}                         # make password hash

class User_Login_Form(ModelForm):
    class Meta:
        model = My_User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}                         # make password hash

class Group_Form(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dynamic_fields = kwargs.pop('dynamic_fields')
        super(DynamicForm, self).__init__(*args, **kwargs)
        for key, value in dynamic_fields:
            self.fields[key.slug] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=value)

# form = DynamicForm(request.POST, dynamic_fields=context)
# print('------------------------------------------ > ',form)

class CommentForm(forms.Form):
    name = forms

