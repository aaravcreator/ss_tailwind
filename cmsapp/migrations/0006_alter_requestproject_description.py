# Generated by Django 4.1 on 2023-08-04 09:05

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0005_lessons_is_locked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestproject',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
