from django.forms import ModelForm, Textarea
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import gettext_lazy as _
from .models import Episode


class EpisodeForm(ModelForm):
    """
    Form class for users to add an episode to a podcast
    """
    # def __init__(self, *args, **kwargs):
    #     super(EpisodeForm, self).__init__(*args, **kwargs)
    #     self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

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
     