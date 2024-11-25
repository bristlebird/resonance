from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Podcast


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

    **Template:**

    :template:`podcast/podcast_detail.html`
    """

    queryset = Podcast.objects.filter(status=1)
    show = get_object_or_404(queryset, slug=slug)
    episodes = show.podcast_episodes.all().order_by("-created_on")
    episode_count = show.podcast_episodes.filter(status=1).count()

    return render(
        request,
        "podcast/podcast_detail.html",
        {
            "show": show,
            "episodes": episodes,
            "episode_count": episode_count,
        },
    )