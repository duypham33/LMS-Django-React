# Generated by Django 4.1 on 2022-09-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_user_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[("1", "Teacher"), ("2", "Staff"), ("3", "Student")],
                default="1",
                max_length=30,
            ),
        ),
    ]
