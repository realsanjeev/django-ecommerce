# Generated by Django 4.2.6 on 2023-10-28 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='remaining_coupon',
            new_name='remaining_time',
        ),
    ]