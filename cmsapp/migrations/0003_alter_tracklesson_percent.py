# Generated by Django 4.1 on 2023-08-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0002_tracklesson_lesson_number_tracklesson_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracklesson',
            name='percent',
            field=models.IntegerField(default=1),
        ),
    ]