# Generated by Django 3.1.1 on 2020-10-23 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_project_project_dependencies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectfiles',
            name='code',
        ),
    ]
