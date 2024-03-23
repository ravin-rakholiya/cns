# Generated by Django 5.0.2 on 2024-03-23 23:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_user_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderGetInTouch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_contacts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]