# Generated by Django 3.1.1 on 2020-10-23 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201023_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_dependencies',
        ),
    ]