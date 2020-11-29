# Generated by Django 3.1.1 on 2020-11-29 08:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_profile_u_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='u_id',
        ),
        migrations.AddField(
            model_name='profile',
            name='chat_with',
            field=models.ManyToManyField(related_name='chat_before', to=settings.AUTH_USER_MODEL),
        ),
    ]
