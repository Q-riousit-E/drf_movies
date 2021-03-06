from django.forms.models import model_to_dict
from django.db.models.aggregates import Avg
from django.db.models.query import Prefetch, QuerySet
from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Article, Comment, Movie, Genre, SimpleRating, DetailedRating
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer, MovieSearchSerializer, MovieSerializer, GenreSerializer, MovieIndexListSerializer, SimpleRatingSerializer, DetailedRatingSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


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


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def movie_search(request):
    query = request.GET.get('q')
    movies = Movie.objects.none()
    if query:
        if query[0] == '#':
            genres = Genre.objects.prefetch_related(
                'movies', 'movies__simple_ratings').filter(name__contains=query[1:])
            for genre in genres:
                movies = movies | genre.movies.annotate(
                    star_average=Avg('simple_ratings__rating'))
            movies = movies.order_by('-star_average')
        else:
            movies = Movie.objects.prefetch_related(
                'simple_ratings').filter(title__contains=query).annotate(star_average=Avg('simple_ratings__rating')).order_by('-star_average')
    serializer = MovieSearchSerializer(movies, many=True)
    return Response(serializer.data)


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
    action = Genre.objects.prefetch_related(
        'movies', 'movies__simple_ratings').get(number=28)
    action = MovieIndexListSerializer(
        action.movies.annotate(star_average=Avg('simple_ratings__rating')).order_by('-star_average', '-release_date')[:20], many=True)
    # comedy = Genre.objects.prefetch_related(
    #     'movies', 'movies__simple_ratings').get(number=28)
    # comedy = MovieIndexListSerializer(
    #     comedy.movies.annotate(star_average=Avg('simple_ratings__rating')).order_by('-star_average', '-release_date')[:20], many=True)
    animation = Genre.objects.prefetch_related(
        'movies', 'movies__simple_ratings').get(number=16)
    animation = MovieIndexListSerializer(
        animation.movies.annotate(star_average=Avg('simple_ratings__rating')).order_by('-star_average', '-release_date')[:20], many=True)
    romance = Genre.objects.prefetch_related(
        'movies', 'movies__simple_ratings').get(number=10749)
    romance = MovieIndexListSerializer(
        romance.movies.annotate(star_average=Avg('simple_ratings__rating')).order_by('-star_average', '-release_date')[:20], many=True)
    horror = Genre.objects.prefetch_related(
        'movies', 'movies__simple_ratings').get(number=27)
    horror = MovieIndexListSerializer(
        horror.movies.annotate(star_average=Avg('simple_ratings__rating')).order_by('-star_average', '-release_date')[:20], many=True)
    sci_fi = Genre.objects.prefetch_related(
        'movies', 'movies__simple_ratings').get(number=878)
    sci_fi = MovieIndexListSerializer(
        sci_fi.movies.annotate(star_average=Avg('simple_ratings__rating')).order_by('-star_average', '-release_date')[:20], many=True)

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
@permission_classes([])
def movie_recommendation(request):
    if not request.user.is_authenticated or request.user.simple_ratings.count() == 0:
        serializer = MovieSearchSerializer(Movie.objects.annotate(star_average=Avg(
            'simple_ratings__rating')).order_by('-star_average', '-release_date')[:5], many=True)
    else:
        simple_ratings = request.user.simple_ratings.prefetch_related(
            'movie').prefetch_related('movie__genres').order_by('-rating')[:50]
        genre_count = {}
        seen_movie_ids = []
        for simple_rating in simple_ratings:
            seen_movie_ids.append(simple_rating.movie.id)
            genres = simple_rating.movie.genres.all()
            for genre in genres:
                genre_count[genre.name] = genre_count.get(genre.name, 0) + 1
        favorite_genre_name = sorted(
            genre_count.items(), key=lambda x: -x[1])[0][0]
        favorite_genre = Genre.objects.get(name=favorite_genre_name)
        serializer = MovieSearchSerializer(
            favorite_genre.movies.exclude(id__in=seen_movie_ids).annotate(star_average=Avg(
                'simple_ratings__rating')).order_by('-star_average')[:5], many=True)

    return Response(serializer.data)


@ api_view(['GET'])
@ authentication_classes([])
@ permission_classes([])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@ api_view(['GET', 'POST', 'PUT', 'DELETE'])
def movie_simple_rating(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        rating = get_object_or_404(
            SimpleRating, movie=movie, user=request.user)
        serializer = SimpleRatingSerializer(rating)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SimpleRatingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        rating = get_object_or_404(
            SimpleRating, movie=movie, user=request.user)
        rating.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        rating = get_object_or_404(
            SimpleRating, movie=movie, user=request.user)
        serializer = SimpleRatingSerializer(instance=rating, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@ api_view(['GET', 'POST', 'PUT', 'DELETE'])
def movie_detailed_rating(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        rating = get_object_or_404(
            DetailedRating, movie=movie, user=request.user)
        serializer = DetailedRatingSerializer(rating)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DetailedRatingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        rating = get_object_or_404(
            DetailedRating, movie=movie, user=request.user)
        rating.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        rating = get_object_or_404(
            DetailedRating, movie=movie, user=request.user)
        serializer = DetailedRatingSerializer(
            instance=rating, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@ api_view(['GET', 'POST'])
@ permission_classes([])
def article_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        articles = get_list_or_404(Article, movie=movie)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': '????????? ???????????? ???????????? ????????? ?????? ????????? ???????????????.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@ api_view(['GET', 'POST'])
@ permission_classes([])
def review_set_list(request, movie_pk):
    movie = Movie.objects.prefetch_related(
        'simple_ratings', 'detailed_ratings', 'articles').prefetch_related('simple_ratings__user', 'articles__comments').get(pk=movie_pk)
    simple_ratings = movie.simple_ratings.all()

    if not simple_ratings:
        return Response(None)

    detailed_ratings = movie.detailed_ratings.all()
    articles = movie.articles.all()
    users = [simple_rating.user for simple_rating in simple_ratings]
    data = []
    for user in users:
        simple = simple_ratings.get(user=user)
        detailed = detailed_ratings.filter(user=user).first()
        if detailed:
            detailed_rating = {
                'originality': detailed.originality,
                'plot': detailed.plot,
                'characters': detailed.characters,
                'cinematography': detailed.cinematography,
                'music_score': detailed.music_score,
                'entertainment_value': detailed.entertainment_value,
            }
        article = articles.filter(user=user).first()
        if article:
            article_dict = model_to_dict(article)
            article_dict['comment_count'] = article.comments.count()
            article_dict['comment_set'] = CommentSerializer(
                article.comments.order_by('-created_at'), many=True).data
        if not detailed and not article:
            continue
        data.append({
            'user_id': user.id,
            'username': user.username,
            'simple_rating': simple.rating,
            'detailed': detailed_rating if detailed else None,
            'article':  article_dict if article else None,
        })

    return JsonResponse(data, safe=False)


@ api_view(['GET', 'POST'])
def my_article(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ArticleSerializer(get_object_or_404(
        Article, user=request.user, movie=movie))
    return Response(serializer.data)


@ api_view(['GET', 'PUT', 'DELETE'])
@ permission_classes([])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({'error': '????????? ???????????? ???????????? ????????? ?????? ????????? ???????????????.'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user != article.user:
            return Response({'error': '?????? ????????? ????????? ??? ?????? ????????? ????????????.'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'error': '????????? ???????????? ???????????? ????????? ?????? ????????? ???????????????.'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user != article.user:
            return Response({'error': '?????? ???????????? ????????? ??? ?????? ????????? ????????????.'}, status=status.HTTP_403_FORBIDDEN)
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
            return Response({'error': '?????? ????????? ????????? ??? ?????? ????????? ????????????.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        if request.user != comment.user:
            return Response({'error': '?????? ????????? ????????? ??? ?????? ????????? ????????????.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
