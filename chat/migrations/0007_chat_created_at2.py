# Generated by Django 3.2.16 on 2023-02-22 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_chat_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='created_at2',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
