from django.shortcuts import render
from django.views import generic
from .models import Podcast
# from django.http import HttpResponse

# Create your views here.
# def my_podcast(request):
#     return HttpResponse("Hello, Podcaster!")
class PodcastList(generic.ListView):
    queryset = Podcast.objects.all()
    template_name = "podcast_list.html"