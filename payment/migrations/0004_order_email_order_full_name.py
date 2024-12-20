# Generated by Django 5.1.3 on 2024-12-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_remove_order_shipping_info_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
