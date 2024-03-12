# Generated by Django 5.0.2 on 2024-03-11 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_user_progress_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(choices=[(1, 'PEDDING'), (2, 'DISPATCH'), (3, 'ON THE WAY'), (4, 'Delevry'), (5, 'Cancle'), (6, 'Return')], default=1),
        ),
    ]
