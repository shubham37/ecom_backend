# Generated by Django 3.1.2 on 2021-01-01 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=200)),
                ('rating', models.IntegerField(default=1)),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='track_status',
            new_name='current_status',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='payment_option',
            new_name='payment_details',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='price',
            new_name='price_detail',
        ),
        migrations.RemoveField(
            model_name='order',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='order',
            name='measurement_parameter',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='rating',
        ),
        migrations.AddField(
            model_name='order',
            name='orderId',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Order Identifier'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(default=0, verbose_name='Sub Total'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='products',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='review',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='order.orderreview'),
        ),
    ]
