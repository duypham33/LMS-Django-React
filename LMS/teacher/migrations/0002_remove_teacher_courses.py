# Generated by Django 4.1 on 2022-09-12 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teacher", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="teacher", name="courses",),
    ]
