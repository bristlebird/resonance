from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
# class Post(models.Model):
class Podcast(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.ForeignKey(
        # User, on_delete=models.CASCADE, related_name="blog_posts"
        # User, on_delete=models.CASCADE, related_name="podcast_shows, podcast_episodes"
        User, on_delete=models.CASCADE, related_name="podcast_shows"
    )
    author = models.CharField(max_length=200)
    description = models.TextField()
    copyright = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    owner_email = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)