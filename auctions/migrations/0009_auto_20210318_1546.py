# Generated by Django 3.1.7 on 2021-03-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210318_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='current_price',
            field=models.FloatField(blank=True),
        ),
    ]
