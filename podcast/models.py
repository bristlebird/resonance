from django.db import models
from django.contrib.auth.models import User
# from podcast.categories import CATEGORY_CHOICES
# from podcast.languages import LANGUAGE_CHOICES


STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
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
    # primary_category = models.CharField(choices=categories.CATEGORY_CHOICES)
    # secondary_category = models.CharField(choices=categories.CATEGORY_CHOICES)
    copyright = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    # spoken_language = models.CharField(choices=languages.LANGUAGE_CHOICES, default="en")
    owner_name = models.CharField(max_length=200)
    owner_email = models.CharField(max_length=200)
    explicit_content_warning = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)