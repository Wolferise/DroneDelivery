# Generated by Django 3.2.5 on 2021-07-16 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryAPI', '0008_statistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='total_weight_delivered',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
