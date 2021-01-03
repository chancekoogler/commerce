# Generated by Django 3.1.2 on 2020-12-14 00:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='link',
            field=models.ManyToManyField(blank=True, related_name='watchList', to=settings.AUTH_USER_MODEL),
        ),
    ]
