"""
MODELS FOR PODCAST APP
"""
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api

# serve cloudinary files over https to avoid insecure content warnings
cloudinary.config(
    secure=True,
)

STATUS = ((0, "Draft"), (1, "Published"))


class Podcast(models.Model):
    """
    Stores a single podcast entry related to :model: `auth.User`
    and :model: `podcast.Episode`
    """

    PODCAST_TYPES = (
        ("Episodic", "episodic"),
        ("Serial", "serial")
    )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    administrator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default="",
        related_name="podcast_shows")
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(choices=PODCAST_TYPES, default="episodic")
    excerpt = models.TextField(blank=True)
    artwork = CloudinaryField(
        'image',
        default='placeholder',
        folder='resonance/images',
    )
    copyright = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)
    owner_name = models.CharField(max_length=200, blank=True)
    owner_email = models.CharField(max_length=200, blank=True)
    explicit_content_warning = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | added by {self.administrator}"


class Episode(models.Model):
    """
    Stores a single episode entry related to :model: `auth.User`
    and :model: `podcast.Podcast`
    """

    EPISODE_TYPES = (
        ("full", "Normal"),
        ("trailer", "Trailer"),
        ("bonus", "Bonus")
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    podcast = models.ForeignKey(
        Podcast, on_delete=models.CASCADE, related_name="podcast_episodes"
    )
    administrator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default="",
        related_name="podcast_administrator")
    audiofile = CloudinaryField(
        'audio file',
        folder='resonance/audio',
        resource_type='auto',
        format="mp3",
    )
    author = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    type = models.CharField(choices=EPISODE_TYPES, default="Normal")
    season_number = models.PositiveIntegerField(default=1)
    episode_number = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    alt_episode_url = models.URLField(max_length=200, blank=True)
    video_url = models.URLField(max_length=200, blank=True)
    explicit_content_warning = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | added by {self.administrator}"
