# Generated by Django 3.1.2 on 2020-12-01 16:51

from django.db import migrations, models
import django.db.models.deletion
import ecom_backend.utils


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to=ecom_backend.utils.upload_image, verbose_name='Upload Category Image'),
        ),
        migrations.AddField(
            model_name='category',
            name='is_top_category',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PopularCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_title', models.CharField(blank=True, max_length=10, null=True)),
                ('banner', models.ImageField(blank=True, null=True, upload_to=ecom_backend.utils.upload_image, verbose_name='Upload Category Image')),
                ('redirection', models.URLField(blank=True, null=True, verbose_name='Redirect To')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
        ),
    ]
