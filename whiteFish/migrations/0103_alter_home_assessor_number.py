# Generated by Django 4.1.1 on 2022-12-06 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whiteFish', '0102_firestation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='assessor_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
