from . import views
from django.urls import path

urlpatterns = [
    path('', views.PodcastList.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<slug:slug>/', views.podcast_detail, name='podcast_detail'),
    path('<slug:slug>/edit-episode/<int:episode_id>',
        views.episode_edit, name='episode_edit'),
    path('<slug:slug>/add-episode',
        views.episode_add, name='episode_add'),
    path('<slug:slug>/delete-episode/<int:episode_id>',
        views.episode_delete, name='episode_delete'),
]