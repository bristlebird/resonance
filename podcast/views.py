from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .models import Podcast, Episode
from .forms import EpisodeForm


class PodcastList(generic.ListView):
    """
    Returns all published podcasts in :model:`podcast.Podcast`
    and displays them in a page of six podcasts. 

    **Context**

    ``queryset``
        All published instances of :model:`podcast.Podcast`
    ``paginate_by``
        Number of podcasts per page.
        
    **Template:**

    :template:`podcast/index.html`
    """

    queryset = Podcast.objects.filter(status=1).order_by("-created_on")
    template_name = "podcast/index.html"
    paginate_by = 6


def podcast_detail(request, slug):
    """
    Display an individual :model:`podcast.Podcast`.

    **Context**

    ``show``
        An instance of :model:`podcast.Podcast`.
    ``epsiodes``
        All epsiodes related to the podcast.
    ``epsiode_count``
        Number of published episodes related to the podcast.
    ``epsiode_form``
        An instance of :form: `podcast.EpisodeForm`

    **Template:**

    :template:`podcast/podcast_detail.html`
    """

    queryset = Podcast.objects.filter(status=1)
    show = get_object_or_404(queryset, slug=slug)
    episodes = show.podcast_episodes.all().order_by("-episode_number")
    episode_count = show.podcast_episodes.filter(status=1).count()

    if request.method == "POST":
        episode_form = EpisodeForm(data=request.POST)
        if episode_form.is_valid():
            episode = episode_form.save(commit=False)
            episode.administrator = request.user
            episode.podcast = show
            episode.slug = slugify(episode.title)
            episode.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Episode added!'
            )

    episode_form = EpisodeForm()

    return render(
        request,
        "podcast/podcast_detail.html",
        {
            "show": show,
            "episodes": episodes,
            "episode_count": episode_count,
            "episode_form": episode_form,
        },
    )


def episode_edit(request, slug, episode_id):
    """
    Display an individual episode to edit

    **Context**

    ``podcast``
        An instance of :model: `podcast.Podcast`
    ``episode``
        A single episode related to the podcast.
    ``episode_form``
        An instance of :form: `podcast.EpisodeForm`
    """
    if request.method == "POST":

        queryset = Podcast.objects.filter(status=1)
        podcast = get_object_or_404(queryset, slug=slug)
        episode = get_object_or_404(Episode, pk=episode_id)
        episode_form = EpisodeForm(data=request.POST, instance=episode)

        # check form is valid and logged in user is podcast admin 
        # (not episode admin)
        if episode_form.is_valid() and podcast.administrator == request.user:
            episode = episode_form.save(commit=False)
            episode.podcast = podcast
            # episode.approved = False
            episode.save()
            messages.add_message(request, messages.SUCCESS, 'Episode Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating episode!')

    return HttpResponseRedirect(reverse('podcast_detail', args=[slug]))


def episode_delete(request, slug, episode_id):
    """
    Delete an individual episode

    **Context**

    ``podcast``
        An instance of :model: `podcast.Podcast`
    ``episode``
        A single episode related to the podcast.
    """
    queryset = Podcast.objects.filter(status=1)
    podcast = get_object_or_404(queryset, slug=slug)
    episode = get_object_or_404(Episode, pk=episode_id)

    if podcast.administrator == request.user:
        episode.delete()
        messages.add_message(request, messages.SUCCESS, 'Episode deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own episodes!')

    return HttpResponseRedirect(reverse('podcast_detail', args=[slug]))


# dashboard access is available to logged in users only
@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    Display content added by logged in user:
    - list of podcasts :model:`podcast.Podcast`.
    - list of epsiodes :model:`podcast.Episode`.

    **Context**

    ``shows``
        All instances of :model:`podcast.Podcast` added by user.
    ``episodes``
        All instances of :model:`podcast.Episode` added by user.

    **Template:**

    :template:`podcast/dashboard.html`
    """    
    # user = get_object_or_404(User, user=request.user)
    user = request.user
    shows = user.podcast_shows.all()
    show_count = shows.count()
    episodes = user.podcast_administrator.all()
    episode_count = episodes.count()

    return render(
        request,
        "podcast/dashboard.html",
        {
            "shows": shows,
            "show_count": show_count,
            "episodes": episodes,
            "episode_count": episode_count,
            # "episode_form": episode_form,
        },
    )
