# Generated by Django 4.1.5 on 2023-03-23 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0039_alter_blog_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="url_image",
            field=models.URLField(blank=True, null=True),
        ),
    ]
