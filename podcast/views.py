from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Podcast
# from django.http import HttpResponse

# Create your views here.
# def my_podcast(request):
#     return HttpResponse("Hello, Podcaster!")
class PodcastList(generic.ListView):
    queryset = Podcast.objects.filter(status=1).order_by("-created_on")
    template_name = "podcast/index.html"
    paginate_by = 6


def podcast_detail(request, slug):
    """
    Display an individual :model:`podcast.Podcast`.

    **Context**

    ``post``
        An instance of :model:`podcast.Podcas`.

    **Template:**

    :template:`podcast/podcast_detail.html`
    """

    queryset = Podcast.objects.filter(status=1)
    show = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "podcast/podcast_detail.html",
        {"show": show},
    )