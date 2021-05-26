from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Movie(models.Model):
    adult = models.BooleanField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path1 = models.CharField(max_length=200)
    poster_path2 = models.CharField(max_length=200)
    poster_path3 = models.CharField(max_length=200)
    poster_path4 = models.CharField(max_length=200)
    trailer_path = models.CharField(max_length=300, null=True)
    release_date = models.DateField()
    director_name = models.CharField(max_length=100, null=True)
    cast1_name = models.CharField(max_length=100, null=True)
    cast2_name = models.CharField(max_length=100, null=True)
    cast3_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'({self.pk}) {self.title}'


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='articles')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='articles')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.pk}) {self.user.usernamne}\'s review about {self.movie.title}'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.pk}) {self.user}\'s comment on review about {self.movie.title}'


class Genre(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)
    movies = models.ManyToManyField(Movie, related_name='genres')

    def __str__(self):
        return f'({self.pk}) {self.name}'


class SimpleRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='simple_ratings')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='simple_ratings')
    rating = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'], name='unique_simple_rating')
        ]

    def __str__(self):
        return f'({self.pk}) {self.user.username}\'s simple rating about {self.movie.title}'


class DetailedRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='detailed_ratings')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='detailed_ratings')
    originality = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    plot = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    cinematography = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    music_score = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    characters = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    entertainment_value = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'], name='unique_detailed_rating')
        ]

    def __str__(self):
        return f'({self.pk}) {self.user.username}\'s detailed rating about {self.movie.title}'
