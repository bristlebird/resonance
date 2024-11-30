from django.forms import ModelForm, Textarea
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import gettext_lazy as _
from .models import Episode, Podcast


class EpisodeForm(ModelForm):
    """
    Form class for users to add an episode to a podcast
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Episode
        fields = ('title', 'description', 'audiofile', 'author', 'keywords',
            'type', 'season_number', 'episode_number', 'alt_episode_url', 
            'video_url', 'explicit_content_warning', 'status')
        labels = {
            'author': _('Podcast creator'),
        }
        widgets = {
            'description': SummernoteWidget(),
        }
     

class PodcastForm(ModelForm):
    """
    Form class for users to add a podcast
    """
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
    
