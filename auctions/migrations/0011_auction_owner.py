# Generated by Django 3.1.2 on 2020-12-30 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20201227_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='owner',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
