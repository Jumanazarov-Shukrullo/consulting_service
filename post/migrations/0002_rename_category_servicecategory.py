# Generated by Django 4.2.1 on 2023-06-08 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='ServiceCategory',
        ),
    ]
