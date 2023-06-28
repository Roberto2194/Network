from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    userFollowing = models.ManyToManyField("User", blank=True, related_name="followed_by")
    postLikes = models.ManyToManyField("Post", blank=True, related_name="liked_by")

        
class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @property
    def likes(self):
        return self.liked_by.count()
    
    @property
    def liked(self, user):
        return self.liked_by.contains(user)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.liked_by.count()
        }
    
    def __str__(self):
        return f"{self.author}: \"{self.body}\""
    