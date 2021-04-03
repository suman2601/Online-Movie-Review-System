from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.details, name="details"),
    path('addmovies/', views.add_movie, name="add_movie"),
    path('updatemovies/<int:id>/', views.update_movie, name="update_movie"),
    path('deletemovies/<int:id>/', views.delete_movie, name="delete_movie"),
    path('addreview/<int:id>/', views.add_review, name="add_review"),
    path('editreview/<int:movie_id>/<int:review_id>/', views.edit_review, name="edit_review"),
    path('deletereview/<int:movie_id>/<int:review_id>/', views.delete_review, name="delete_review"),
    path('watchlistadd/<int:movie_id>/', views.watchlist_add, name="watchlist_add"),
    path('watchlistdel/<int:movie_id>/', views.watchlist_del, name="watchlist_del"),
    path('watchlistview/', views.watchlist_view, name="watchlist_view"),


]