# Generated by Django 2.2 on 2020-01-21 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectviewed',
            name='user_session_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]