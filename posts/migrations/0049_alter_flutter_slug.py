# Generated by Django 4.1.5 on 2023-08-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0048_alter_blog_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flutter",
            name="slug",
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]
