# Generated by Django 5.0.2 on 2024-03-19 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_provideravailability_providerservice_servicebooking_and_more'),
        ('user', '0002_address_emailverification_delete_login_main_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerservice',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.address'),
        ),
        migrations.AddField(
            model_name='providerservice',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.servicecategory'),
        ),
        migrations.AddField(
            model_name='providerservice',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='provideravailability',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.providerservice'),
        ),
        migrations.AddField(
            model_name='servicebooking',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.address'),
        ),
        migrations.AddField(
            model_name='servicebooking',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.providerservice'),
        ),
        migrations.AddField(
            model_name='servicebooking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='servicerating',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.servicebooking'),
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='State',
        ),
        migrations.DeleteModel(
            name='ServicePost',
        ),
        migrations.DeleteModel(
            name='ServicePostComment',
        ),
        migrations.DeleteModel(
            name='ServiceProviderAvailability',
        ),
        migrations.DeleteModel(
            name='UserService',
        ),
        migrations.DeleteModel(
            name='UserServiceRating',
        ),
    ]
