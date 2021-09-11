# Generated by Django 3.1.6 on 2021-09-09 06:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='like_count',
            field=models.BigIntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='video',
            name='likes',
            field=models.ManyToManyField(blank=True, default='None', related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
