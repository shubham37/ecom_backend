# Generated by Django 3.1.2 on 2021-01-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20210103_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Title')),
                ('discount_amount', models.IntegerField(verbose_name='Amount')),
                ('discount_type', models.CharField(choices=[('FLAT', 'FLAT'), ('PERCENTAGE', 'PERCENTAGE')], default='FLAT', max_length=15, verbose_name='Discount Type')),
                ('products', models.ManyToManyField(null=True, to='product.Product')),
            ],
        ),
        migrations.RemoveField(
            model_name='discountoptions',
            name='discount_option_group',
        ),
        migrations.RemoveField(
            model_name='productoptions',
            name='brands_option',
        ),
        migrations.RemoveField(
            model_name='productoptions',
            name='discounts',
        ),
        migrations.RemoveField(
            model_name='productoptions',
            name='features',
        ),
        migrations.RemoveField(
            model_name='productoptions',
            name='price_range_group',
        ),
        migrations.RemoveField(
            model_name='productoptions',
            name='quantity_option',
        ),
        migrations.RemoveField(
            model_name='productoptions',
            name='shipping_option',
        ),
        migrations.DeleteModel(
            name='DiscountOptionGroups',
        ),
        migrations.DeleteModel(
            name='DiscountOptions',
        ),
        migrations.DeleteModel(
            name='ProductOptions',
        ),
    ]
