# Generated by Django 4.0.5 on 2022-10-21 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_python_html_ide'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='html',
            name='ide',
        ),
        migrations.AddField(
            model_name='html',
            name='level',
            field=models.TextField(blank=True, default='Easy'),
        ),
        migrations.AddField(
            model_name='html',
            name='summer_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
