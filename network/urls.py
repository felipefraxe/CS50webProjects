
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API routes
    path("new_post", views.send_post, name="send_post"),
    path("show_post/<str:watchers>/<int:user_id>", views.show_post, name="show_post"),
    path("like", views.like, name="like"),
    path("profile/<int:user_id>", views.load_profile, name="load_profile"),
    path("follow", views.follow, name="follow"),
    path("edit_post", views.edit_post, name="edit_post")
]
