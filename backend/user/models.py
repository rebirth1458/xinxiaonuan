from datetime import timezone

from django.db import models
from rest_framework import serializers


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=255, verbose_name="密码")
    avatar = models.CharField(max_length=255, null=True, verbose_name="用户头像")
    create_time = models.DateTimeField( null=True,verbose_name="创建时间")
    update_time = models.DateTimeField(null=True, verbose_name="更新时间")
    class Meta:
        db_table = 'user'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class Session(models.Model):
    id=models.AutoField(primary_key=True)
    session_id = models.IntegerField(null=True, db_index=True)
    message=models.TextField()
    class Meta:
        db_table = 'session'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class UserSession(models.Model):
    user_session_id = models.AutoField(primary_key=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id', verbose_name="用户id")
    session_id = models.IntegerField(db_index=True, null=True)
    class Meta:
        db_table = 'user_session'

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = '__all__'