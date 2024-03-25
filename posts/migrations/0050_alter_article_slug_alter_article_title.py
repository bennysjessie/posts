# Generated by Django 4.1.5 on 2023-08-28 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0049_alter_flutter_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
