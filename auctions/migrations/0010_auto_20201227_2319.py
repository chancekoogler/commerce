# Generated by Django 3.1.2 on 2020-12-27 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201224_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='itemBid',
        ),
        migrations.AddField(
            model_name='bids',
            name='auction',
            field=models.ManyToManyField(blank=True, related_name='auction', to='auctions.Auction'),
        ),
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.CharField(default='', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid',
            field=models.FloatField(),
        ),
    ]