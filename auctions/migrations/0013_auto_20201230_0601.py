# Generated by Django 3.1.2 on 2020-12-30 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auction_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='closed',
        ),
        migrations.AddField(
            model_name='auction',
            name='isOpen',
            field=models.BooleanField(default=True),
        ),
    ]
