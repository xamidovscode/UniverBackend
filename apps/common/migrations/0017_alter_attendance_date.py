# Generated by Django 4.2.11 on 2024-08-30 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_alter_attendance_date_alter_studentpayments_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 30, 21, 13, 49, 875349), verbose_name='Date'),
        ),
    ]