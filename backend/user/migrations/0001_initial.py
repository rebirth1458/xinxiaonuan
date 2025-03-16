# Generated by Django 5.1.2 on 2025-03-16 08:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.IntegerField(db_index=True, null=True)),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'session',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('avatar', models.CharField(max_length=255, null=True, verbose_name='用户头像')),
                ('create_time', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(null=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('user_session_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.IntegerField(db_index=True, null=True)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='用户id')),
            ],
            options={
                'db_table': 'user_session',
            },
        ),
    ]
