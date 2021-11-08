from django.db import models
from django.db.models import manager
from common_utils.base_entity import BaseModel
from django.contrib.auth.models import User
# Create your models here.

class ProfileType(BaseModel):
    name = models.CharField(max_length=300,unique=True)

    def __str__(self):
        return self.name
        
    class Meta:
        managed = True
        db_table = 'profile_type'


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    type = models.ForeignKey(ProfileType, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username

    class Meta:
        managed = True
        db_table = 'profile'


class ProfileDetails(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.profile

    class Meta:
        managed = True
        db_table = 'profile_details'

class My_User(User):
    full_name = models.CharField(max_length=300, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'my_user'


class Secret_Key(BaseModel):
    s_key = models.CharField(max_length=300, blank=False, null=False)
    s_name = models.CharField(max_length=300, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'secret_key'