# Generated by Django 4.0.5 on 2022-10-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_alter_python_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='python',
            name='level',
            field=models.CharField(default='Easy', max_length=10),
        ),
        migrations.AlterField(
            model_name='python',
            name='tags',
            field=models.TextField(blank=True, null=True),
        ),
    ]
