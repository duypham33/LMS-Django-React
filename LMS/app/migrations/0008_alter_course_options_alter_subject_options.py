# Generated by Django 4.1 on 2022-09-12 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_alter_course_title"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="course", options={"ordering": ["subject", "coursenum"]},
        ),
        migrations.AlterModelOptions(name="subject", options={"ordering": ["name"]},),
    ]