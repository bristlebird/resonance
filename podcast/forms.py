from django import forms
from django.forms import ModelForm, Textarea
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Episode, Podcast


class EpisodeForm(ModelForm):
    """
    Form class for users to add an episode to a podcast
    """
    # display audiofile cloudinaryField as a clearableFileInput, 
    # so that file can be removed and/or replaced after uploading
    # https://stackoverflow.com/questions/14336925/how-to-not-render-django-image-field-currently-and-clear-stuff
    audiofile = forms.FileField(required=False, error_messages = {'invalid':_("Mp3 audio files only")}, widget=forms.ClearableFileInput)

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
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         'title',
    #         'audiofile',
    #         Row(
    #             Column('author', css_class='form-group col-md-6 mb-0'),
    #             Column('keywords', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('type', css_class='form-group col-md-6 mb-0'),
    #             Column('season_number', css_class='form-group col-md-4 mb-0'),
    #             Column('episode_number', css_class='form-group col-md-2 mb-0'),
    #             css_class='form-row'
    #         ),
    #         'description',
    #         Row(
    #             Column('alt_episode_url', css_class='form-group col-md-6 mb-0'),
    #             Column('video_url', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ), 
    #         Row(
    #             Column('explicit_content_warning', css_class='form-group col-md-6 mb-0'),
    #             Column('status', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         )
    #     )
     

class PodcastForm(ModelForm):
    """
    Form class for users to add a podcast
    """
    artwork = forms.ImageField(required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.ClearableFileInput)
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
        }
    
