from . import views
from django.urls import path

urlpatterns = [
    path('', views.PodcastList.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<slug:slug>/', views.podcast_detail, name='podcast_detail'),
    path('<slug:slug>/edit_episode/<int:episode_id>',
        views.episode_edit, name='episode_edit'),
]