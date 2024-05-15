# Generated by Django 5.0.3 on 2024-05-15 05:22

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                (
                    "deleted_by_cascade",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("full_name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255, null=True, unique=True)),
                ("gender", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "marital_status",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("nationality", models.CharField(default="Egypt", max_length=255)),
                ("national_id", models.CharField(max_length=255, unique=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("address", models.JSONField(blank=True, null=True)),
                ("phone", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("speciality", models.CharField(max_length=255)),
                (
                    "license_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "experience_years",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("work_days", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                (
                    "deleted_by_cascade",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("full_name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255, null=True, unique=True)),
                ("gender", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "marital_status",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("nationality", models.CharField(default="Egypt", max_length=255)),
                ("national_id", models.CharField(max_length=255, unique=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("address", models.JSONField(blank=True, null=True)),
                ("phone", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                (
                    "deleted_by_cascade",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("full_name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255, null=True, unique=True)),
                ("gender", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "marital_status",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("nationality", models.CharField(default="Egypt", max_length=255)),
                ("national_id", models.CharField(max_length=255, unique=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("address", models.JSONField(blank=True, null=True)),
                ("phone", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "disease_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("blood_type", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserImage",
            fields=[
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                (
                    "deleted_by_cascade",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("image", models.ImageField(upload_to="user_images")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="image",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
