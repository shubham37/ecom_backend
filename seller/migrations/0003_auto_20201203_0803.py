# Generated by Django 3.1.2 on 2020-12-03 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('seller', '0002_auto_20201203_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerdetail',
            name='bank_city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.city'),
        ),
    ]
