# Generated by Django 4.1 on 2022-09-12 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_alter_course_options_alter_subject_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="session_year", options={"ordering": ["start_date"]},
        ),
    ]