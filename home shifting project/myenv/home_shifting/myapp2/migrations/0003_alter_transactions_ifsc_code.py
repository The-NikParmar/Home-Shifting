# Generated by Django 5.0.2 on 2024-03-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp2', '0002_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='ifsc_code',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
