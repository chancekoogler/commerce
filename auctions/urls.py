from django.urls import path

from . import views

urlpatterns = [
    path("", views.listings, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings", views.listings, name="listings"),
    path("<int:item_id>", views.item, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:item_id>/close", views.closeAuction, name="closeAuction"),
    path("category", views.category, name="category"),
    path("<str:category>", views.itemsOfCat, name="itemsOfCat")
]
