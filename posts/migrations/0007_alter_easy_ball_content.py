# Generated by Django 4.0.5 on 2022-10-19 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_remove_blog_read_min_blog_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='easy_ball',
            name='content',
            field=models.TextField(),
        ),
    ]
