# Generated by Django 4.1 on 2024-01-09 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0013_eventregister'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregister',
            name='School_or_College_name',
            field=models.CharField(max_length=200),
        ),
    ]