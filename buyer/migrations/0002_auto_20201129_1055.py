# Generated by Django 3.1.2 on 2020-11-29 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='alternate_mobile',
            new_name='alternative_mobile',
        ),
    ]
