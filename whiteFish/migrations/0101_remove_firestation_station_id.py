# Generated by Django 4.1.1 on 2022-11-15 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whiteFish', '0100_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firestation',
            name='station_id',
        ),
    ]