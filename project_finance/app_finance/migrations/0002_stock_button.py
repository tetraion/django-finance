# Generated by Django 4.0.6 on 2022-07-29 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='button',
            field=models.IntegerField(default=1),
        ),
    ]
