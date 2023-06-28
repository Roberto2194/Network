
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),

    # API Routes
    path("create", views.create, name="create"),
    path("like", views.like, name="like"),
    path("edit", views.edit, name="edit")
]
