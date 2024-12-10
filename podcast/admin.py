from django.contrib import admin
from .models import Podcast, Episode
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Podcast)
class PostAdmin(SummernoteModelAdmin):
    """
    Lists fields to display in admin, fields for search,
    filters, fields to prepopulate and rich-text editor.
    """

    list_display = ('title', 'slug', 'status')
    search_fields = ['title', 'description']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description', 'excerpt',)


@admin.register(Episode)
class EpisodeAdmin(SummernoteModelAdmin):
    """
    Lists fields to display in admin, fields for search,
    filters, fields to prepopulate and rich-text editor.
    """

    list_display = ('title', 'podcast', 'episode_number', 'status')
    search_fields = ['title', 'description']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)
