# Generated by Django 3.2.16 on 2023-02-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0010_auto_20230220_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonetrns_models',
            name='PhoneTrns',
            field=models.IntegerField(verbose_name=''),
        ),
    ]