# Generated by Django 4.2.6 on 2023-10-28 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_rename_apartmart_address_address_apartment_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='apartment_address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
