from django.urls import path

from . import views

urlpatterns = [
    path('search', views.search, name='search'),
    path('show', views.show, name='list'),
    path('links', views.links, name='links'),
    path('status', views.status, name='status'),
]