# Generated by Django 3.1 on 2024-08-07 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20240807_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
