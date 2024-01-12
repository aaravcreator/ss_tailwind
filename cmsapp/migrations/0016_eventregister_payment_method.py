# Generated by Django 4.1 on 2024-01-10 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0015_event_qr_code_eventregister_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregister',
            name='payment_method',
            field=models.CharField(choices=[('KHALTI', 'KHALTI'), ('CASH', 'CASH')], default='CASH', max_length=300),
        ),
    ]