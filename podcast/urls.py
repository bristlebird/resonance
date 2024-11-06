from . import views
from django.urls import path

urlpatterns = [
    path('', views.PodcastList.as_view(), name='home'),
    path('<slug:slug>/', views.podcast_detail, name='podcast_detail'),
]