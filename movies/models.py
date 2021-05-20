from django.db import models
from django.conf import settings

# Create your models here.


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Movie(models.Model):
    adult = models.BooleanField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    release_date = models.DateField()


class Genre(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    movies = models.ManyToManyField(Movie, related_name='genres')
