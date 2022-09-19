# Generated by Django 4.1 on 2022-09-18 23:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0011_notification_from_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="assocusernotice",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="assocusernotice",
            name="date_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="assocusernotice",
            name="notice",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assoc",
                to="app.notification",
            ),
        ),
    ]
