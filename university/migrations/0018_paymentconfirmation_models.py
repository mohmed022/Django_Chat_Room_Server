# Generated by Django 3.2.16 on 2023-02-20 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import university.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('university', '0017_alter_phonetrns_models_name_compony'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentConfirmation_Models',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=1, max_digits=10)),
                ('Apathy', models.ImageField(blank=True, null=True, upload_to=university.models.uplodephoto_Pass)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('Package', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='university.package_models')),
                ('created_by_PaymentConfirmation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by_PaymentConfirmation', to=settings.AUTH_USER_MODEL)),
                ('sections', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='university.sections_models')),
                ('university', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='university.university_models')),
            ],
        ),
    ]