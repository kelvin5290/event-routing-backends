# Generated by Django 2.2.24 on 2021-10-16 09:28

import fernet_fields.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_routing_backends', '0003_auto_20210713_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='routerconfiguration',
            name='auth_key',
            field=fernet_fields.fields.EncryptedCharField(blank=True, max_length=256, null=True, verbose_name='Auth Key'),
        ),
        migrations.AddField(
            model_name='routerconfiguration',
            name='auth_scheme',
            field=models.CharField(choices=[('BASIC', 'Basic'), ('BEARER', 'Bearer')], default='BASIC', max_length=6, verbose_name='Auth Scheme'),
        ),
        migrations.AddField(
            model_name='routerconfiguration',
            name='password',
            field=fernet_fields.fields.EncryptedCharField(blank=True, max_length=256, null=True, verbose_name='Password'),
        ),
        migrations.AddField(
            model_name='routerconfiguration',
            name='username',
            field=fernet_fields.fields.EncryptedCharField(blank=True, max_length=256, null=True, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='routerconfiguration',
            name='backend_name',
            field=models.CharField(choices=[('Caliper', 'Caliper'), ('xAPI', 'xAPI')], db_index=True, default='xAPI', help_text='Name of the tracking backend on which this router should be applied.<br/>Please note that this field is <b>case sensitive.</b>', max_length=50),
        ),
    ]