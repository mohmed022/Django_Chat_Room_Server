# Generated by Django 3.2.8 on 2023-05-08 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat3', '0003_auto_20230507_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting_questions',
            name='vote',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='voting_questions',
        ),
        migrations.AddField(
            model_name='vote',
            name='voting_questions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='chat3.voting_questions'),
        ),
    ]
