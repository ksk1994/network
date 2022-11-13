from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    post = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="likes")

    def likes_count(self):
        return self.likes.count()
    

    def __str__(self):
        return f"{self.id} {self.user} {self.post} {self.time} {self.likes}"


class Profile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="profile")
    following = models.ForeignKey("User", blank=True, null=True, on_delete=models.PROTECT, related_name="following")
    def __str__(self):
        return f"{self.id} {self.user} {self.following}"

    def is_valid_profile(self):
        return self.user != self.following