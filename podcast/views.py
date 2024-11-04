from django.shortcuts import render
from django.views import generic
from .models import Podcast
# from django.http import HttpResponse

# Create your views here.
# def my_podcast(request):
#     return HttpResponse("Hello, Podcaster!")
class PodcastList(generic.ListView):
    queryset = Podcast.objects.filter(status=1).order_by("-created_on")
    template_name = "podcast_list.html"