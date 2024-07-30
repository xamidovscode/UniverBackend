# Generated by Django 5.0.6 on 2024-07-30 08:16

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_alter_floor_options_alter_application_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='user_apartment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='common.userapartment'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 30, 13, 16, 0, 672459), verbose_name='Date'),
        ),
    ]
