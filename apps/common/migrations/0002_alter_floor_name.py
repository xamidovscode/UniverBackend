# Generated by Django 5.0.4 on 2024-05-01 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floor',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
    ]
