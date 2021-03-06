# Generated by Django 3.1.1 on 2020-12-10 09:12

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_auto_20201208_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Online',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_seen', models.DateTimeField(default=django.utils.timezone.now)),
                ('online_users', models.ManyToManyField(related_name='online', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
