"""
CLASSES TO DISPLAY MODELS IN DJANGO ADMIN
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import About


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """
    Adds rich-text editing of about content in admin
    """
    summernote_fields = ('content',)
