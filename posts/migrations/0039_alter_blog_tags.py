# Generated by Django 4.1.5 on 2023-02-24 22:18

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0038_delete_loggedinuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
