# Generated by Django 3.2.16 on 2023-02-20 10:50

from django.db import migrations, models
import university.models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0018_paymentconfirmation_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentconfirmation_models',
            name='Apathy',
            field=models.ImageField(blank=True, null=True, upload_to=university.models.uplodephoto_Apathy),
        ),
    ]
