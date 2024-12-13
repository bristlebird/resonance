"""
APP CONFIG
"""
from django.apps import AppConfig


class PodcastConfig(AppConfig):
    """
    Provides primary key type for podcast app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'podcast'
