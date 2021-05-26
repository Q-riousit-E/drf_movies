from django.db.models.aggregates import Avg
from rest_framework import serializers
from .models import Article, Comment, DetailedRating, Movie, Genre, SimpleRating


class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Article
        fields = ('id', 'content', 'username', 'user')
        read_only_fields = ('user', 'movie',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article', 'user',)


class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(
        source='comment_set.count', read_only=True)
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Article
        fields = ('id', 'content', 'username',
                  'user', 'comment_set', 'comment_count')
        read_only_fields = ('user', 'movie',)


class MovieSerializer(serializers.ModelSerializer):
    star_average = serializers.SerializerMethodField()
    simple_rating_counts = serializers.SerializerMethodField()
    detailed_ratings_average = serializers.SerializerMethodField()
    genre_names = serializers.SerializerMethodField()

    def get_star_average(self, obj):
        average = obj.simple_ratings.all().aggregate(
            Avg('rating')).get('rating__avg') or 0
        average = round(average, 1)
        return average

    def get_simple_rating_counts(self, obj):
        ratings = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
        rating_counts = {
            ratings[i]: obj.simple_ratings.filter(rating=ratings[i]).count() for i in range(len(ratings))
        }

        return rating_counts

    def get_detailed_ratings_average(self, obj):
        detailed_ratings = {
            'originality_average': obj.detailed_ratings.all().aggregate(Avg('originality')).get('originality__avg') or 0,
            'plot_average': obj.detailed_ratings.all().aggregate(Avg('plot')).get('plot__avg') or 0,
            'characters_average': obj.detailed_ratings.all().aggregate(Avg('characters')).get('characters__avg') or 0,
            'cinematography_average': obj.detailed_ratings.all().aggregate(Avg('cinematography')).get('cinematography__avg') or 0,
            'music_score_average': obj.detailed_ratings.all().aggregate(Avg('music_score')).get('music_score__avg') or 0,
            'entertainment_value_average': obj.detailed_ratings.all().aggregate(Avg('entertainment_value')).get('entertainment_value__avg') or 0,
        }
        for key, value in detailed_ratings.items():
            if key:
                detailed_ratings[key] = round(detailed_ratings.get(key), 1)
        return detailed_ratings

    def get_genre_names(self, obj):
        genres = obj.genres.all()
        genre_names = [genres[i].name for i in range(len(genres))]
        return genre_names

    class Meta:
        model = Movie
        fields = '__all__'


class MovieIndexListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'poster_path', 'trailer_path', 'director_name',
                  'cast1_name', 'cast2_name', 'cast3_name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('movies',)


class SimpleRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimpleRating
        fields = '__all__'
        read_only_fields = ('movie', 'user',)


class DetailedRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetailedRating
        fields = '__all__'
        read_only_fields = ('movie', 'user')


class MovieSearchSerializer(serializers.ModelSerializer):
    star_average = serializers.SerializerMethodField()
    genre_names = serializers.SerializerMethodField()

    def get_star_average(self, obj):
        average = obj.simple_ratings.all().aggregate(
            Avg('rating')).get('rating__avg') or 0
        average = round(average, 1)
        return average

    def get_genre_names(self, obj):
        genres = obj.genres.all()
        genre_names = [genres[i].name for i in range(len(genres))]
        return genre_names

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'star_average',
                  'release_date', 'genre_names',)
