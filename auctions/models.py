from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(default="No Category Listed",max_length=64)
    category_link = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    creators = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creators")
    bidder = models.ForeignKey(User,default=True, on_delete=models.PROTECT, related_name="bidder")
    listing_status = models.BooleanField(default=True)
    item = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    bid = models.FloatField(default=0)
    link = models.CharField(default="https://cdn-icons-png.flaticon.com/512/3125/3125669.png",max_length=128)
    group = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now)
    

    def __str__(self):
        return f"{self.creators} {self.bidder} {self.listing_status} {self.item} {self.description} {self.price} {self.bid} {self.link} {self.group}"

class Comment(models.Model):
    comment = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="writer")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="get_comments")

    def __str__(self):
        return f"{self.writer} {self.listing} {self.comment}"

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.PROTECT, related_name="watcher")
    watchlist = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watcher} {self.watchlist}"