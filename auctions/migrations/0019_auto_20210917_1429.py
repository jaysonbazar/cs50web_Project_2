# Generated by Django 3.2.6 on 2021-09-17 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_category_category_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bidder',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(),
        ),
    ]
