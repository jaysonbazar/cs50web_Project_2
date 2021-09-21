# Generated by Django 3.2.6 on 2021-08-28 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_group_listing_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='type',
        ),
        migrations.AddField(
            model_name='listing',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
            preserve_default=False,
        ),
    ]
