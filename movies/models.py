from django.db import models
from django.conf import settings
from django.db.models.fields import FloatField

# Create your models here.


class Movie(models.Model):
    adult = models.BooleanField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    trailer_path = models.CharField(max_length=300, null=True)
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    release_date = models.DateField()
    director_name = models.CharField(max_length=100, null=True)
    cast1_name = models.CharField(max_length=100, null=True)
    cast2_name = models.CharField(max_length=100, null=True)
    cast3_name = models.CharField(max_length=100, null=True)


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)
    movies = models.ManyToManyField(Movie, related_name='genres')


class SimpleRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()


class DetailedRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    originality = models.FloatField()
    plot = models.FloatField()
    cinematography = models.FloatField()
    music_score = models.FloatField()
    characters = models.FloatField()
    entertainment_value = models.FloatField()
