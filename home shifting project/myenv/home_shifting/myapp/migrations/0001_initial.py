# Generated by Django 5.0.2 on 2024-03-12 10:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=40)),
                ('uemail', models.EmailField(max_length=254)),
                ('ucontact', models.CharField(max_length=15)),
                ('upassword', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('htype', models.CharField(max_length=40, null=True)),
                ('bname', models.CharField(max_length=40)),
                ('movefrom', models.CharField(max_length=40)),
                ('moveto', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=40)),
                ('zipcode', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.PositiveIntegerField()),
                ('razorpay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('house-type', 'house-type'), ('Booking', 'Booking'), ('payment-status', 'payment-status'), ('on-the-way', 'on-the-way'), ('cancel', 'Cancle'), ('finish', 'finish process')], default='Booking', max_length=20)),
                ('house_type_active', models.BooleanField(default=False)),
                ('booking_active', models.BooleanField(default=False)),
                ('payment_status_active', models.BooleanField(default=False)),
                ('on_the_way_active', models.BooleanField(default=False)),
                ('cancel_active', models.BooleanField(default=False)),
                ('finish_active', models.BooleanField(default=False)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
