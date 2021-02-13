from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.details, name="details"),
    path('addmovies/', views.add_movie, name="add_movie"),
    path('updatemovies/<int:id>/', views.update_movie, name="update_movie"),
    path('deletemovies/<int:id>/', views.delete_movie, name="delete_movie"),
]