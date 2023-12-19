# Generated by Django 4.1 on 2023-12-19 18:53

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0007_alter_user_email_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('banner', models.ImageField(default='event.jpg', upload_to='event_banners')),
                ('scheduled_date', models.DateTimeField()),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('location', models.CharField(max_length=200)),
                ('event_fee', models.IntegerField(default=0)),
                ('is_free', models.BooleanField(default=False)),
                ('seats', models.IntegerField(default=0)),
                ('rules', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('syllabus', models.FileField(upload_to='syllabus')),
                ('status', models.CharField(choices=[('ONGOING', 'ONGOING'), ('UPCOMING', 'UPCOMING')], default='UPCOMING', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
