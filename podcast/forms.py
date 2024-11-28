from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from .models import Episode


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
        # widgets = {
        #     'description': Textarea(attrs={'cols': 80, 'rows': 20}),
        # }
        labels = {
            'author': _('Podcast creator'),
        }
        # help_text = {
        #     'audiofile': _('mp3 audio files under 10MB only'),
        # }
     