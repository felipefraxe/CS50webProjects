from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("category=<int:category_id>", views.index_category, name="index_category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sell", views.sell, name="sell"),
    path("item/<int:item_id>", views.item, name="item"),
    path("item/<int:item_id>/watch", views.watch, name="watch"),
    path("item/<int:item_id>/comment", views.comment, name="comment"),
    path("item/<int:item_id>/bid", views.bid, name="bid"),
    path("item/<int:item_id>/close", views.close,name="close"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist")
]
