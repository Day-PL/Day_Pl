# Generated by Django 4.2.3 on 2023-08-25 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0006_rename_expected_time_place_expected_time_during_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="plan",
            old_name="user_id",
            new_name="user",
        ),
    ]
