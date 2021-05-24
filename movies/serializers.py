from django.db.models.aggregates import Avg
from rest_framework import serializers
from .models import Article, Comment, DetailedRating, Movie, Genre, SimpleRating


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
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

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'movie',)


class MovieSerializer(serializers.ModelSerializer):
    star_average = serializers.SerializerMethodField()

    def get_star_average(self, obj):
        average = obj.simple_ratings.all().aggregate(Avg('rating')).get('rating__avg')
        if average == None:
            return 0
        return average

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
