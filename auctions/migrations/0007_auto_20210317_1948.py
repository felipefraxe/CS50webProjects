# Generated by Django 3.1.7 on 2021-03-17 23:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_item_watchers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
