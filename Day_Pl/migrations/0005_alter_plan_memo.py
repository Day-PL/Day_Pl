# Generated by Django 4.2.3 on 2023-08-22 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0004_place_lat_place_lng_alter_place_contact_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="memo",
            field=models.TextField(null=True),
        ),
    ]
