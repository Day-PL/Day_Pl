# Generated by Django 4.2.3 on 2023-08-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0017_plan_view_users"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userplanview",
            name="created_at",
        ),
        migrations.AddField(
            model_name="userplanview",
            name="view_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
