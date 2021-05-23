from django.db.models import manager
from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Article, Comment, Movie, Genre
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer, MovieSerializer, GenreSerializer, MovieIndexListSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

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


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def movie_index(request):
    # Action, Animation, Comedy, Horror, Romance, Science Fiction
    genre_ids = [28, 16, 35, 27, 10749, 878]
    action = MovieIndexListSerializer(
        get_object_or_404(Genre, number=28).movies.order_by('-release_date')[:20], many=True)
    animation = MovieIndexListSerializer(
        get_object_or_404(Genre, number=16).movies.order_by('-release_date')[:20], many=True)
    # comedy = MovieIndexListSerializer(
    #     get_object_or_404(Genre, number=35).movies.order_by('-release_date')[:20], many=True)
    horror = MovieIndexListSerializer(
        get_object_or_404(Genre, number=27).movies.order_by('-release_date')[:20], many=True)
    romance = MovieIndexListSerializer(
        get_object_or_404(Genre, number=10749).movies.order_by('-release_date')[:20], many=True)
    sci_fi = MovieIndexListSerializer(
        get_object_or_404(Genre, number=878).movies.order_by('-release_date')[:20], many=True)

    data = {
        'action': action.data,
        'animation': animation.data,
        # 'comedy': comedy.data,
        'horror': horror.data,
        'romance': romance.data,
        'sci_fi': sci_fi.data,
    }

    return JsonResponse(data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([])
def article_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        articles = get_list_or_404(Article, movie=movie)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': '리뷰를 작성하기 위해서는 사용자 인증 정보가 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@ api_view(['GET', 'PUT', 'DELETE'])
@ permission_classes([])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({'error': '리뷰를 삭제하기 위해서는 사용자 인증 정보가 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user != article.user:
            return Response({'error': '해당 리뷰를 삭제할 수 있는 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'error': '리뷰를 수정하기 위해서는 사용자 인증 정보가 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user != article.user:
            return Response({'error': '해당 게시물을 수정할 수 있는 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@ api_view(['POST'])
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@ api_view(['PUT', 'DELETE', ])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'DELETE':
        if request.user != comment.user:
            return Response({'error': '해당 댓글을 삭제할 수 있는 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        if request.user != comment.user:
            return Response({'error': '해당 댓글을 수정할 수 있는 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
