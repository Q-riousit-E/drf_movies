from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('genres/', views.genre_list),
    path('genres/<int:genre_number>/movie/', views.genre_add_movie),
    path('movies/', views.movie_list),
    path('movies/index/', views.movie_index),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/comments/', views.create_comment),
    path('articles/<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail),
]
