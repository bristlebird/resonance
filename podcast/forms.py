from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget
from .models import Episode, Podcast
# from cloudinary.models import CloudinaryField
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Field, Submit, Row, Column


class PodcastForm(ModelForm):
    """
    Form class for users to add a podcast
    """
    artwork = forms.FileField(
        required=False,
        error_messages = {'invalid':_("Image files only")},
        widget=forms.ClearableFileInput
    )
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Podcast
        fields = (
            'title',
            'description',
            'excerpt',
            'artwork',
            'type',
            'author',
            'copyright',
            'keywords',
            'website',
            'owner_name',
            'owner_email',
            'explicit_content_warning',
            'status',
        )
        labels = {
            'author': _('Podcast creator'),
        }
        widgets = {
            'description': SummernoteWidget(),
            'excerpt': SummernoteWidget(),
        }


class EpisodeForm(ModelForm):
    """
    Form class for users to add an episode to a podcast
    """
    # display audiofile cloudinaryField as a clearableFileInput,
    # so that file can be removed and/or replaced after uploading
    # https://stackoverflow.com/questions/14336925/how-to-not-render-django-image-field-currently-and-clear-stuff
    audiofile = forms.FileField(
        required=False,
        error_messages = {'invalid':_("Mp3 audio files only")},
        widget=forms.ClearableFileInput
    )

    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Episode
        fields = (
            'title',
            'audiofile',
            'author',
            'keywords',
            'type',
            'season_number',
            'episode_number',
            'description',
            'alt_episode_url',
            'video_url',
            'explicit_content_warning',
            'status',
        )
        labels = {
            'author': _('Podcast creator'),
            'audiofile': _('Audio file'),
        }
        widgets = {
            'description': SummernoteWidget(),
        }
