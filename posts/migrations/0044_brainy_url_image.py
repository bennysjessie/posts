# Generated by Django 4.1.5 on 2023-03-29 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0043_alter_article_url_image_alter_blog_url_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="brainy",
            name="url_image",
            field=models.URLField(blank=True, null=True),
        ),
    ]
