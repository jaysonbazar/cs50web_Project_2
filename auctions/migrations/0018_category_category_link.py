# Generated by Django 3.2.6 on 2021-09-17 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_watchlist_watcher'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_link',
            field=models.CharField(default=True, max_length=128),
            preserve_default=False,
        ),
    ]
