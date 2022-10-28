# Generated by Django 4.1 on 2022-10-27 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatapi", "0003_alter_message_options_chat_roomname"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chat", options={"ordering": ["-latestSent"]},
        ),
        migrations.AddField(
            model_name="chat",
            name="latestSent",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]