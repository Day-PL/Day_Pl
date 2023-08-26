# Generated by Django 4.2.3 on 2023-08-25 03:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Day_Pl", "0009_alter_plan_removed_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="like_users",
            field=models.ManyToManyField(
                related_name="plans", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
