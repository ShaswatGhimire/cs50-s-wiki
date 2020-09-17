from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.titlesearch, name="header"),
    path("search",views.search,name="search"),
    path("newpage",views.newpage,name="newpage"),
    path("wiki/<str:head>/edit",views.edit,name="edit"),
    path("randompage",views.randompage,name="randompage")
]
