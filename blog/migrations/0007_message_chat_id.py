# Generated by Django 3.1.1 on 2020-12-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_notifyme_room_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='chat_id',
            field=models.CharField(default='something new', max_length=400),
            preserve_default=False,
        ),
    ]