# Generated by Django 5.0.2 on 2024-03-14 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='truckpartner',
            name='package_name',
        ),
        migrations.AddField(
            model_name='truckpartner',
            name='package_type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='truckpartner',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
