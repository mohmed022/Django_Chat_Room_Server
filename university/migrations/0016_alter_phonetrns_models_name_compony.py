# Generated by Django 3.2.16 on 2023-02-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0015_alter_phonetrns_models_name_compony'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonetrns_models',
            name='Name_Compony',
            field=models.CharField(choices=[('vodafone', 'Vodafone'), ('orange', 'Orange'), ('etisalat', 'Etisalat'), ('bank', 'Bank')], default='vodafone', max_length=20),
        ),
    ]