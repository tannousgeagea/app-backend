# Generated by Django 4.2 on 2024-08-04 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ImageMode",
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
                ("mode", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Image Mode",
                "db_table": "image_mode",
            },
        ),
        migrations.CreateModel(
            name="ProjectType",
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
                ("project_type", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("meta_info", models.JSONField(blank=True, null=True)),
            ],
            options={
                "verbose_name_plural": "Project Type",
                "db_table": "project_type",
            },
        ),
        migrations.CreateModel(
            name="Project",
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
                ("project_id", models.CharField(max_length=255)),
                ("project_name", models.CharField(max_length=255)),
                ("annotation_group", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("meta_info", models.JSONField(blank=True, null=True)),
                (
                    "project_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="database.projecttype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Project",
                "db_table": "project",
            },
        ),
        migrations.CreateModel(
            name="Image",
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
                ("image_id", models.CharField(max_length=255)),
                ("image_name", models.CharField(max_length=255)),
                ("image_file", models.ImageField(upload_to="images/")),
                ("annotated", models.BooleanField(default=False)),
                ("processed", models.BooleanField(default=False)),
                (
                    "mode",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="database.imagemode",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="database.project",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Images",
                "db_table": "image",
            },
        ),
    ]