# Generated by Django 3.2.6 on 2021-08-28 22:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='link',
            field=models.CharField(default=django.utils.timezone.now, max_length=128),
            preserve_default=False,
        ),
    ]
