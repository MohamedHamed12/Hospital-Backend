# Generated by Django 5.0.3 on 2024-05-02 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_address_user_alter_phone_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="marital_status",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="marital_status",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="marital_status",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]