# Generated by Django 4.1.5 on 2023-08-25 17:18

import ckeditor.fields
import ckeditor_uploader.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0046_alter_blog_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="title",
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.CreateModel(
            name="Flutter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("level", models.CharField(default="Easy", max_length=30)),
                ("category", models.CharField(default="coding", max_length=100)),
                ("title", models.TextField(max_length=255)),
                ("keyword", models.TextField(blank=True, null=True)),
                ("tags", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "content",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True
                    ),
                ),
                ("url_image", models.URLField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "updated",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                ("slug", models.SlugField(max_length=150, unique=True)),
                ("draft", models.BooleanField(default=False)),
                (
                    "allow_comments",
                    models.BooleanField(default=True, verbose_name="allow comments"),
                ),
                ("publish", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tag",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "ordering": ("-publish",),
            },
        ),
    ]