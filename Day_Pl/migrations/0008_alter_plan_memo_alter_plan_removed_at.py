# Generated by Django 4.2.3 on 2023-08-25 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0007_rename_user_id_plan_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="memo",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="plan",
            name="removed_at",
            field=models.DateTimeField(null=True),
        ),
    ]
