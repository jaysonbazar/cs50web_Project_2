# Generated by Django 3.2.6 on 2021-09-18 00:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20210917_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]