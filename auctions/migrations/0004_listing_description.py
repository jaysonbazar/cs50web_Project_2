# Generated by Django 3.2.6 on 2021-08-28 10:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210828_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
