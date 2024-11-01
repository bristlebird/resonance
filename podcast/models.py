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
    artwork = models.CharField(max_length=200, default='path/to/image/file')
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

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | added by {self.author}"


class Episode(models.Model):

    EPISODE_TYPES = (
        ("Normal", "Normal"), 
        ("Trailer", "Trailer"),
        ("Bonus", "Bonus")
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    podcast = models.ForeignKey(
        Podcast, on_delete=models.CASCADE, related_name="podcast_episodes"
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_episodes"
    )
    author = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    type = models.CharField(choices=EPISODE_TYPES, default="Normal")
    season_number = models.IntegerField(default=1)
    episode_number = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    artwork = models.CharField(max_length=200, blank=True)
    alt_episode_url = models.CharField(max_length=200, blank=True)
    video_url = models.CharField(max_length=200, blank=True)
    explicit_content_warning = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | added by {self.creator}"
