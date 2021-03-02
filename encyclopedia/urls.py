from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
]
