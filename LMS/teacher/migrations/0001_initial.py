# Generated by Django 4.1 on 2022-09-12 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app", "0004_session_year_subject_course"),
        ("student", "0001_initial"),
        ("staff", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "courses",
                    models.ManyToManyField(related_name="instructors", to="app.course"),
                ),
                (
                    "staffs",
                    models.ManyToManyField(related_name="hosts", to="staff.staff"),
                ),
                (
                    "students",
                    models.ManyToManyField(
                        related_name="teachers", to="student.student"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
