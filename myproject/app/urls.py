from django.urls import path

from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('movies/', movies, name='movies'),
    path('reviews/', reviews, name='reviews'),
    path('search/', search, name='search'),
    path('show/', search, name='show'),
]
