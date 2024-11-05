from django.contrib import admin
from .models import Podcast, Episode
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Podcast)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)


# Register your models here.
admin.site.register(Episode)
