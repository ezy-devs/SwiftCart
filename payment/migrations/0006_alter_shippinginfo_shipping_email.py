# Generated by Django 5.1.3 on 2024-12-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_shippinginfo_shipping_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippinginfo',
            name='shipping_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
