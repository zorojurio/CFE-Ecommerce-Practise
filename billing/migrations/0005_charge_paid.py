# Generated by Django 2.2 on 2020-01-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_auto_20200122_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
