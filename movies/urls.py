from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('genres/', views.genre_list),
    path('movies/', views.movie_list),
    path('movies/index/', views.movie_index),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/simple_rating/', views.movie_simple_rating),
    path('movies/<int:movie_pk>/articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/comments/', views.create_comment),
    path('comments/<int:comment_pk>/', views.comment_detail),
]
