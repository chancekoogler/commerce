from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return str(self.title)
    
class Auction(models.Model):
    title = models.CharField(max_length=75)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    price = models.IntegerField()
    watchList = models.ManyToManyField(User, blank=True, related_name="watchList")
    owner = models.CharField(max_length=80)
    isOpen = models.BooleanField(default=True)
    winner = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    
    
    def __str__(self):
        return self.title


class Bids(models.Model):
    bid = models.FloatField()
    user = models.CharField(max_length=80)
    auction = models.ManyToManyField(Auction, blank=True, related_name="auction")

    def __str__(self):
        return str(self.bid)
    
class Comments(models.Model):
    user = models.CharField(max_length=80)
    comment = models.CharField(max_length=650)
    auction = models.ManyToManyField(Auction, blank=True, related_name="comments")
    
    def __str__(self):
        return str(self.comment)

    
