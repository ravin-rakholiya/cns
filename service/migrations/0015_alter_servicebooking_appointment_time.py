# Generated by Django 5.0.2 on 2024-03-25 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0014_alter_providerservice_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicebooking',
            name='appointment_time',
            field=models.CharField(max_length=128),
        ),
    ]