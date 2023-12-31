# Generated by Django 4.2.3 on 2023-08-20 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0003_rename_address_dong_place_address_lo"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="lat",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="place",
            name="lng",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="place",
            name="contact",
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name="place",
            name="rating",
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name="planplace",
            name="place",
            field=models.ForeignKey(
                blank=True,
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="Day_Pl.place",
            ),
        ),
    ]
