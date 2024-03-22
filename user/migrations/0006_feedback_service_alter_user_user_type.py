# Generated by Django 5.0.2 on 2024-03-19 22:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_providerservice_address_providerservice_category_and_more'),
        ('user', '0005_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.servicebooking'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.usertype'),
        ),
    ]