# Generated by Django 4.2.1 on 2023-06-08 08:35

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_laws_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laws',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
