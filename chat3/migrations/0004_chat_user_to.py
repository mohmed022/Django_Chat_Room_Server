# Generated by Django 3.2.9 on 2023-03-26 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat3', '0003_chat_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='user_to',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='user_to', to='users.newuser'),
            preserve_default=False,
        ),
    ]
