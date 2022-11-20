# Generated by Django 4.0.6 on 2022-07-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
            ],
        ),
    ]
