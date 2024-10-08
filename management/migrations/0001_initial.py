# Generated by Django 5.1 on 2024-08-13 01:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('apk_file', models.FileField(upload_to='apks/', verbose_name='APK File')),
                ('first_screen_shot', models.ImageField(upload_to='f_screenshot/', verbose_name='First Screenshot')),
                ('second_screen_shot', models.ImageField(upload_to='s_screenshot/', verbose_name='Second Screenshot')),
                ('video_recording', models.FileField(upload_to='video_recording/', verbose_name='Video Recording')),
                ('ui_hierarchy', models.TextField(blank=True, null=True, verbose_name='UI Hierarchy')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_uploaded_by', to=settings.AUTH_USER_MODEL, verbose_name='Uploaded by')),
            ],
        ),
    ]
