# Generated by Django 5.1.3 on 2024-12-30 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_category_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='created_by',
            new_name='user',
        ),
    ]
