# Generated by Django 4.1.7 on 2023-03-12 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0005_remove_booking_typeofticketandprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bookingDate',
            field=models.DateField(auto_now=True),
        ),
    ]
