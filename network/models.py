from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    following = models.ManyToManyField(User, blank=True, default=None, related_name="flow")
    followers = models.ManyToManyField(User, blank=True, default=None, related_name="supporters")


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    post = models.CharField(max_length=280)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date.strftime('%b %d %Y, %I:%M %p')}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "user_id": self.user.id,
            "post": self.post,
            "date": self.date.strftime("%I:%M %p · %b %d, %Y"),
            "likes": self.likes.count()
        }