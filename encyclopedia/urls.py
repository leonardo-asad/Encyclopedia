from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:article>", views.entries, name="entries"),
    path("/random", views.random, name="random"),
    path("/create", views.create, name="create"),
    path("/edit", views.edit, name="edit")
]
