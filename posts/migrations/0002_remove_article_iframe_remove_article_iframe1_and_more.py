# Generated by Django 4.0.5 on 2022-09-30 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='iframe',
        ),
        migrations.RemoveField(
            model_name='article',
            name='iframe1',
        ),
        migrations.RemoveField(
            model_name='article',
            name='iframe2',
        ),
    ]
