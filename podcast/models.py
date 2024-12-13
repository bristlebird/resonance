from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
# from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api
# from resonance import categories

# # configure cloudinary to serve files over https to avoid mixed / insecure content warnings
cloudinary.config(
  secure = True,
)



# For testing model validation:
# https://github.com/cloudinary/cloudinary-django-sample/blob/master/photo_album/models.py
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 50  # 50mb


def file_validation(file):
    if not file:
        raise ValidationError("No file selected.")

    # For regular upload, we get UploadedFile instance, so we can validate it.
    # When using direct upload from the browser, here we get an instance of
    # the CloudinaryResource and file is already uploaded to Cloudinary.
    # Still can perform all kinds on validations and maybe delete file,
    # approve moderation, perform analysis, etc.
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 50MB.")
        if file.format != 'mp3':
            raise ValidationError("File must be in mp3 format.")


# from podcast.categories import CATEGORY_CHOICES
# from podcast.languages import LANGUAGE_CHOICES

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.


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
        User, on_delete=models.CASCADE, default="", related_name="podcast_shows"
    )
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(choices=PODCAST_TYPES, default="episodic")
    excerpt = models.TextField(blank=True)
    artwork = CloudinaryField(
        'image',
        default='placeholder',
        folder='resonance/images',
    )
    # primary_category = models.CharField(choices=categories.CATEGORY_CHOICES)
    # secondary_category = models.CharField(choices=categories.CATEGORY_CHOICES)
    copyright = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)
    # spoken_language = models.CharField(choices=languages.LANGUAGE_CHOICES, default="en")
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
        ("Normal", "Normal"),
        ("Trailer", "Trailer"),
        ("Bonus", "Bonus")
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    podcast = models.ForeignKey(
        Podcast, on_delete=models.CASCADE, related_name="podcast_episodes"
    )
    administrator = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", related_name="podcast_administrator"
    )
    audiofile = CloudinaryField(
        'audio file',
        # default='placeholder',
        folder='resonance/audio',
        resource_type='auto',
        format="mp3",
        # validators=[file_validation],
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
