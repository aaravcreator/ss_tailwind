# Generated by Django 4.1 on 2023-08-04 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0004_requestproject_alter_tracklesson_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='is_locked',
            field=models.BooleanField(default=True),
        ),
    ]
