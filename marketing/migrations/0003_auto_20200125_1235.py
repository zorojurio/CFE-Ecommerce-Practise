# Generated by Django 2.2 on 2020-01-25 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_marketingpreference_mailchimp_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketingpreference',
            name='mailchimp_subscribed',
            field=models.NullBooleanField(),
        ),
    ]
