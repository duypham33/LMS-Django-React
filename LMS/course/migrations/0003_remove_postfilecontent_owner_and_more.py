# Generated by Django 4.1 on 2022-09-22 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0002_page_postfilecontent"),
    ]

    operations = [
        migrations.RemoveField(model_name="postfilecontent", name="owner",),
        migrations.RemoveField(model_name="postfilecontent", name="page",),
        migrations.DeleteModel(name="Page",),
        migrations.DeleteModel(name="PostFileContent",),
    ]
