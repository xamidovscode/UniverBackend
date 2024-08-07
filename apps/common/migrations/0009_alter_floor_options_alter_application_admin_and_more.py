# Generated by Django 5.0.6 on 2024-07-30 08:15

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_latereason_attendance_admin_attendance_reason_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='floor',
            options={},
        ),
        migrations.AlterField(
            model_name='application',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 30, 13, 15, 18, 797239), verbose_name='Date'),
        ),
    ]
