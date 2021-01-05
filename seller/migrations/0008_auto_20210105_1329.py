# Generated by Django 3.1.2 on 2021-01-05 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0007_auto_20210104_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='identifier',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Seller Identifer'),
        ),
        migrations.AddField(
            model_name='sellerdetail',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sellerdetail',
            name='pincodes',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='sellerdetail',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sellerdetail',
            name='bank_city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sellerdetail',
            name='branch',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sellerdetail',
            name='zip_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
