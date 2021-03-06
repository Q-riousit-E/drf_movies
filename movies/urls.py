from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('genres/', views.genre_list),
    path('movie/search/', views.movie_search),
    path('movies/', views.movie_list),
    path('movies/index/', views.movie_index),
    path('movies/recommendation/', views.movie_recommendation),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/simple-rating/', views.movie_simple_rating),
    path('movies/<int:movie_pk>/detailed-rating/', views.movie_detailed_rating),
    path('movies/<int:movie_pk>/articles/', views.article_list),
    path('movies/<int:movie_pk>/review-sets/', views.review_set_list),
    path('movies/<int:movie_pk>/my-article/', views.my_article),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/comments/', views.create_comment),
    path('comments/<int:comment_pk>/', views.comment_detail),
]
