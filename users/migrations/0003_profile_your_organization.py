# Generated by Django 3.1.1 on 2020-10-24 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_cover_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='your_organization',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]