# Generated by Django 4.1 on 2022-09-28 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0013_assignmentfile_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="closed",
            field=models.BooleanField(default=False),
        ),
    ]
