# Generated by Django 4.2.3 on 2023-08-28 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0018_remove_userplanview_created_at_userplanview_view_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plan",
            name="removed",
        ),
    ]
