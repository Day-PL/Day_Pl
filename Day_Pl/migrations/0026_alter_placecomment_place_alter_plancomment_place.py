# Generated by Django 4.2.3 on 2023-09-10 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Day_Pl", "0025_placecomment_comment_plancomment_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="placecomment",
            name="place",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="Day_Pl.place",
            ),
        ),
        migrations.AlterField(
            model_name="plancomment",
            name="place",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="Day_Pl.plan",
            ),
        ),
    ]