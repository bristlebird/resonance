from django import forms
from .models import Episode


class EpisodeForm(forms.ModelForm):
    """
    Form class for users to add an episode to a podcast
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Episode
        fields = ('title', 'description',)