# Generated by Django 3.2.16 on 2023-02-14 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='about',
            field=models.TextField(blank=True, max_length=500, verbose_name='about'),
        ),
    ]
