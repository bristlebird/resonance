from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .models import Podcast, Episode
from .forms import EpisodeForm, PodcastForm
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
if not os.getenv('CLOUDINARY_API_SECRET'):
    raise Exception('CLOUDINARY_API_SECRET environment variable is not set.')

# configure cloudinary to serve files over https to avoid mixed / insecure content warnings
cloudinary.config(
  cloud_name = 'bristlebird',
  api_key = '566277371789765',
  api_secret = os.getenv('CLOUDINARY_API_SECRET'),
  secure = True,
)




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
    ``episodes``
        All episodes related to the podcast.
    ``episode_count``
        Number of published episodes related to the podcast.
    ``episode_form``
        An instance of :form: `podcast.EpisodeForm`

    **Template:**

    :template:`podcast/podcast_detail.html`
    """

    # queryset = Podcast.objects.filter(status=1)
    queryset = Podcast.objects.all()
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

# dashboard access is available to logged in users only
@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    Display content added by logged in user:
    - list of podcasts :model:`podcast.Podcast`.
    - list of episodes :model:`podcast.Episode`.

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

# dashboard access is available to logged in users only
@login_required(login_url='/accounts/login/')
def podcast_add(request):
    """
    Add a new podcast :model:`podcast.Podcast`.

    **Context**

    ``podcast``
        An instance of :model: `podcast.Podcast`
    ``podcast_form``
        An instance of :form: `podcast.PodcastForm`
    **Template:**

    :template:`podcast/podcast_add.html`
    """    
    if request.method == "POST":
        podcast_form = PodcastForm(request.POST, request.FILES)
        if podcast_form.is_valid():
            podcast = podcast_form.save(commit=False)
            podcast.administrator = request.user
            podcast.slug = slugify(podcast.title)
            podcast.save()
            messages.add_message(
                request, messages.SUCCESS, 'Podcast added!')
            return HttpResponseRedirect(reverse('podcast_detail', args=[podcast.slug]))  
        else:
            messages.add_message(
                request, messages.ERROR, 'Error adding podcast!')

    podcast_form = PodcastForm()
    context = {
        # "podcast": podcast,
        "podcast_form": podcast_form,
    }
    return render(request, "podcast/podcast_add.html", context)


@login_required(login_url='/accounts/login/')
def episode_add(request, slug):
    """
    Add a new episode to a show

    **Context**

    ``podcast``
        An instance of :model: `podcast.Podcast`
    ``episode``
        A single episode related to the podcast.
    ``episode_form``
        An instance of :form: `podcast.EpisodeForm`
    """

    queryset = Podcast.objects.all()
    show = get_object_or_404(queryset, slug=slug)
    if request.method == "POST":
        episode_form = EpisodeForm(request.POST, request.FILES)
        if episode_form.is_valid() and show.administrator == request.user:
            episode = episode_form.save(commit=False)
            episode.administrator = request.user
            episode.podcast = show
            episode.slug = slugify(episode.title)
            # print("files in request(add) = ",request.FILES)
            episode.save()
            messages.add_message(
                request, messages.SUCCESS, 'Episode added!')
            return HttpResponseRedirect(reverse('podcast_detail', args=[slug]))  
        else:
            messages.add_message(
                request, messages.ERROR, 'Error adding episode!')

    episode_form = EpisodeForm()
    context = {
        "show": show,
        # "episode": episode,
        "episode_form": episode_form,
    }
    return render(request, "podcast/episode_add.html", context)



@login_required(login_url='/accounts/login/')
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

    queryset = Podcast.objects.all()
    show = get_object_or_404(queryset, slug=slug)
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.method == "POST":
        episode_form = EpisodeForm(request.POST, request.FILES, instance=episode)
        if episode_form.is_valid() and show.administrator == request.user:
            print("files in request(edit) = ",request.FILES)
            episode = episode_form.save(commit=False)
            episode.administrator = request.user
            episode.podcast = show
            episode.slug = slugify(episode.title)
            episode.save()
            messages.add_message(
                request, messages.SUCCESS, 'Episode Updated!')
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating episode!')

    episode_form = EpisodeForm(instance=episode)
    context = {
        "show": show,
        "episode": episode,
        # "episodes": episodes,
        "episode_form": episode_form,
    }
    return render(request, "podcast/episode_edit.html", context)


def episode_edit_onpage(request, slug, episode_id):
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


@login_required(login_url='/accounts/login/')
def episode_delete(request, slug, episode_id):
    """
    Delete an individual episode

    **Context**

    ``podcast``
        An instance of :model: `podcast.Podcast`
    ``episode``
        A single episode related to the podcast.
    """
    queryset = Podcast.objects.all()
    podcast = get_object_or_404(queryset, slug=slug)
    episode = get_object_or_404(Episode, pk=episode_id)

    if podcast.administrator == request.user:
        episode.delete()
        messages.add_message(request, messages.SUCCESS, 'Episode deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own episodes!')

    return HttpResponseRedirect(reverse('podcast_detail', args=[slug]))


