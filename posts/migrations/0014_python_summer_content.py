# Generated by Django 4.0.5 on 2022-10-21 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_python_level_alter_html_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='python',
            name='summer_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
