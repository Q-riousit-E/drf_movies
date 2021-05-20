from django.shortcuts import get_list_or_404, get_object_or_404
from django.core import serializers
from .models import Article, Comment, Movie, Genre
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer, MovieSerializer, GenreSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Create your views here.


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def genre_list(request):
    if request.method == 'GET':
        genres = get_list_or_404(Genre)
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def genre_add_movie(request, genre_number):
    genre = get_object_or_404(Genre, number=genre_number)
    movie_id = request.data.get('movie_id')
    print(movie_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    genre.movies.add(movie)
    data = {
        'success': True,
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.data.get('user_id'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        article.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user_id=request.data.get('user_id'), article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE', ])
@authentication_classes([])
@permission_classes([])
def comment_detail(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'DELETE':
        comment.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
