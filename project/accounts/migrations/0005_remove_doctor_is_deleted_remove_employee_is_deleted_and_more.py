# Generated by Django 5.0.3 on 2024-05-13 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_doctor_deleted_doctor_deleted_by_cascade_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctor",
            name="is_deleted",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="is_deleted",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="is_deleted",
        ),
    ]