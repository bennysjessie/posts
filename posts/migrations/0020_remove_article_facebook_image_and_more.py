# Generated by Django 4.0.5 on 2022-11-18 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_academic_description_ask_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='facebook_image',
        ),
        migrations.RemoveField(
            model_name='article',
            name='youtube_image',
        ),
    ]
