from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=144, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")
    image_url = models.CharField(max_length=5000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    is_closed = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name="taker")
    start_price = models.FloatField()
    current_price = models.FloatField(blank=True, default=None)
    date = models.DateField(default=timezone.now)
    watchers = models.ManyToManyField(User, blank=True, related_name="user")

    def __str__(self):
        return f"{self.title} - ${self.start_price:.2f} - ${self.current_price}"


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} - {self.user} - ${self.offer:.2f}"


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=400)
    comment_date = models.DateTimeField(default=timezone.now)