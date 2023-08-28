# Generated by Django 4.2.3 on 2023-08-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0012_plan_total_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="planplace",
            name="expected_time_from_this",
        ),
        migrations.AlterField(
            model_name="place",
            name="expected_time_during",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="place",
            name="period_end",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="place",
            name="period_start",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="place",
            name="review_total",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="place",
            name="url",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
