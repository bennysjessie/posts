# Generated by Django 4.1.5 on 2023-01-09 20:14

import ckeditor_uploader.fields
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("posts", "0028_alter_article_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="body",
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name="article",
            name="tag",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="title",
            field=models.CharField(max_length=300, null=True),
        ),
    ]
