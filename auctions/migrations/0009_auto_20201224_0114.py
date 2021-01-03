# Generated by Django 3.1.2 on 2020-12-24 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20201224_0050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='itemBid',
        ),
        migrations.AddField(
            model_name='bids',
            name='itemBid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
            preserve_default=False,
        ),
    ]