# Generated by Django 4.2.6 on 2023-10-28 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='apartmart_address',
            new_name='apartment_address',
        ),
    ]