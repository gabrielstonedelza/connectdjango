# Generated by Django 3.1.1 on 2020-11-05 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_tutorial_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]