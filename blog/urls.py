from django.urls import path

from . import views
from .feeds import LatestThoughts

urlpatterns = [
    path("", views.home, name="home"),
    path("thoughts/", views.thoughts, name="thoughts"),
    path("thoughts/<int:pk>/", views.thought_detail, name="thought_detail"),
    path("about/", views.about, name="about"),
    path("search/", views.search, name="search"),
    path("search/live/", views.search_live, name="search_live"),
    path("feed/", LatestThoughts(), name="feed"),
]
