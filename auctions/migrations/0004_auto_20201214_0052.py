# Generated by Django 3.1.2 on 2020-12-14 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='link',
            new_name='watchList',
        ),
    ]