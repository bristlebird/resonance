"""
PODCAST APP VIEWS

- PodcastList: displays list of published podcasts on the home page
— podcast_detail: displays individual podcast & list of associated episodes
— dashboard: displays list of podcasts added by loggged in user
- podcast_add: allows logged in user to add new podcast
- podcast_edit: allows logged in user to edit existing podcast details
- podcast_delete: allows logged in user to delete existing podcast
- episode_add: allows logged in user to add new episode
- episode_edit: allows logged in user to edit existing episode details
- episode_delete: allows logged in user to delete existing episode

"""
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied
# Import the Cloudinary libraries
# ===============================
import cloudinary
import cloudinary.uploader
import cloudinary.api
from .models import Podcast, Episode
from .forms import EpisodeForm, PodcastForm

# Set Cloudinary to serve files
# over https to avoid mixed / insecure content warnings
# ===============================
cloudinary.config(
    cloud_name='bristlebird',
    secure=True
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
    
    # should only display published podcasts that have episodes with audio 
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

    **Template:**

    :template:`podcast/podcast_detail.html`
    """

    # queryset = Podcast.objects.all()
    queryset = Podcast.objects.all()
    show = get_object_or_404(queryset, slug=slug)
    episodes = show.podcast_episodes.all().order_by("episode_number")
    episode_count = show.podcast_episodes.filter(status=1).count()


    # get collection of published episodes with audio for RSS feed
    feed_episodes = show.podcast_episodes.filter(
        status=1,
        audiofile__contains="resonance/audio"
    ).order_by("-episode_number")

    # throw 403 if no results, i.e. no published episodes with audio available
    show_feed = True if feed_episodes else False

    # To display Podcast subscribe button with link to RSS feed:
    # - podcast must be published &
    # — audio file uploaded to at least 1 published episode
    # for episode in episodes:
    #     audio_available = False
    #     if 'resonance/audio' in episode.audiofile.url:
    #         audio_available = True
    #         break

    # if audio_available == False and show.status == 0:
    #     raise PermissionDenied


    return render(
        request,
        "podcast/podcast_detail.html",
        {
            "show": show,
            "episodes": episodes,
            "episode_count": episode_count,
            "show_feed": show_feed,
        },
    )


def podcast_feed(request, slug):
    """
    Output podcast RSS feed from :model:`podcast.Podcast`
    when podcast is published & episode published with audio

    **Context**

    ``show``
        An instance of :model:`podcast.Podcast`.
    ``episodes``
        All published episodes related to the podcast.

    **Template:**

    :template:`podcast/podcast_feed.xml`
    """


    queryset = Podcast.objects.all()
    show = get_object_or_404(queryset, slug=slug)
    # throw 403 if show in draft 
    # if show.status == 0 and show.administrator != request.user:
    if show.status == 0:
        raise PermissionDenied

    # podcast published so get collection of published episodes with audio
    episodes = show.podcast_episodes.filter(
        status=1,
        audiofile__contains="resonance/audio"
    ).order_by("-episode_number")

    # throw 403 if no results, i.e. no published episodes with audio available
    if not episodes:
        raise PermissionDenied

    # if more than 1 season, season number should be displayed
    for episode in episodes:
        if episode.season_number > 1:
            multiple_seasons = True
            break
        else:
            multiple_seasons = False

    return render(
        request,
        "podcast/podcast_feed.xml",
        {
            "show": show,
            "episodes": episodes,
            "multiple_seasons": multiple_seasons,
        },
        content_type="text/xml",
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
    user = request.user
    shows = user.podcast_shows.all()
    episodes = user.podcast_administrator.all()

    return render(
        request,
        "podcast/dashboard.html",
        {
            "shows": shows,
            "episodes": episodes,
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
            # print("files in request(add) = ", request.FILES)
            podcast.save()
            messages.add_message(
                request, messages.SUCCESS, 'Podcast added!')
            return HttpResponseRedirect(
                reverse('podcast_detail', args=[podcast.slug]))
        else:
            messages.add_message(
                request, messages.ERROR, 'Error adding podcast!')

    podcast_form = PodcastForm()
    context = {
        "podcast_form": podcast_form,
    }
    return render(request, "podcast/podcast_add.html", context)


@login_required(login_url='/accounts/login/')
def podcast_edit(request, podcast_id):
    """
    Display an individual podcast to edit

    **Context**

    ``podcast``
        An instance of :model: `podcast.Podcast`
    ``podcast_form``
        An instance of :form: `podcast.PodcastForm`
    """

    queryset = Podcast.objects.all()
    show = get_object_or_404(queryset, pk=podcast_id)
    # Raise a 403 error if logged in user is not the podcast / show admin
    # https://docs.djangoproject.com/en/5.1/ref/views/#the-403-http-forbidden-view
    if show.administrator != request.user:
        raise PermissionDenied

    if request.method == "POST":
        podcast_form = PodcastForm(
            request.POST, request.FILES, instance=show
        )
        if podcast_form.is_valid() and show.administrator == request.user:
            print("files in request(edit) = ", request.FILES)
            show = podcast_form.save(commit=False)
            show.administrator = request.user
            show.slug = slugify(show.title)
            # if file clear checkbox is selected,
            # image file should be deleted from cloudinary
            show.save()
            messages.add_message(
                request, messages.SUCCESS, 'Podcast updated!')
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating podcast!')

    podcast_form = PodcastForm(instance=show)
    context = {
        "show": show,
        "podcast_form": podcast_form,
    }
    return render(request, "podcast/podcast_edit.html", context)


@login_required(login_url='/accounts/login/')
def podcast_delete(request, slug, podcast_id):
    """
    Delete an individual podcast:
    `slug` needed for podcast urls, `podcast_id` for query

    **Context**

    ``podcast``
        An instance of :model: `podcast.Podcast`
    ``episodes``
        All episodes related to the podcast.
    """

    queryset = Podcast.objects.all()
    # show = get_object_or_404(queryset, slug=slug)
    show = get_object_or_404(queryset, pk=podcast_id)
    episodes = show.podcast_episodes.all()

    # Raise a 403 error if logged in user is not the podcast / show admin
    if show.administrator != request.user:
        raise PermissionDenied
    else:
        for episode in episodes:
            # delete audio files from cloudinary
            # https://cloudinary.com/documentation/image_upload_api_reference#destroy
            # use django cleanup or post_delete signals to delete orphaned file
            if episode.audiofile:
                cloudinary.uploader.destroy(
                    episode.audiofile.public_id,
                    invalidate=True,
                    resource_type="video"
                )
        # no need to specifically delete episodes as deletion handled by
        # on_delete=models.CASCADE in Episode.podcast model when...
        show.delete()
        messages.add_message(
            request, messages.SUCCESS, 'Podcast deleted!'
        )

    return redirect('/dashboard/')


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
    # Raise a 403 error if logged in user is not the podcast / show admin
    if show.administrator != request.user:
        raise PermissionDenied

    if request.method == "POST":
        episode_form = EpisodeForm(request.POST, request.FILES)
        if episode_form.is_valid() and show.administrator == request.user:
            episode = episode_form.save(commit=False)
            episode.administrator = request.user
            episode.podcast = show
            episode.slug = slugify(episode.title)
            print("files in request(add) = ", request.FILES)
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
    # Raise a 403 error if logged in user is not the podcast / show admin
    if show.administrator != request.user:
        raise PermissionDenied

    if request.method == "POST":
        episode_form = EpisodeForm(
            request.POST, request.FILES, instance=episode
        )
        if episode_form.is_valid() and show.administrator == request.user:
            print("files in request(edit) = ", request.FILES)
            episode = episode_form.save(commit=False)
            episode.administrator = request.user
            episode.podcast = show
            episode.slug = slugify(episode.title)
            # if file clear checkbox is selected,
            # audio file should be deleted from cloudinary
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
    show = get_object_or_404(queryset, slug=slug)
    episode = get_object_or_404(Episode, pk=episode_id)
    # Raise a 403 error if logged in user is not the podcast / show admin
    if show.administrator != request.user:
        raise PermissionDenied
    else:
        # delete audio file from cloudinary
        # https://cloudinary.com/documentation/image_upload_api_reference#destroy
        # use django cleanup or post_delete signals to delete orphaned files?
        if episode.audiofile:
            cloudinary.uploader.destroy(
                episode.audiofile.public_id,
                invalidate=True,
                resource_type="video"
            )
        #     print(result)
        # else:
        #     print('no audio to delete')
        episode.delete()
        messages.add_message(
            request, messages.SUCCESS, 'Episode deleted!'
        )

    return HttpResponseRedirect(reverse('podcast_detail', args=[slug]))
