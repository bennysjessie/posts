# Generated by Django 4.0.5 on 2022-10-12 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_easy_ball_tag_easy_ball_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='read_min',
        ),
        migrations.AddField(
            model_name='blog',
            name='level',
            field=models.CharField(default='Easy', max_length=30),
        ),
    ]