# Generated by Django 3.1.1 on 2020-10-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifyme',
            name='blog_id',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='notifyme',
            name='tuto_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]