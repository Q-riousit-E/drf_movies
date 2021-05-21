from movies.models import Movie, Genre
from movies.serializers import MovieSerializer
import requests
from django.core.management.base import BaseCommand


class Scraper:
    BASE_URL = 'https://api.themoviedb.org/3'
    POSTER_BASE_URL = 'https://image.tmdb.org/t/p/original'
    API_KEY = 'b19c89dd8bffcd21e75f82a15020c75c'

    def get_genres(self):
        if Genre.objects.count():
            return
        GENRE_URL = f'{self.BASE_URL}/genre/movie/list'
        params = {'api_key': self.API_KEY}
        res = requests.get(GENRE_URL, params=params)
        genres = res.json()['genres']
        for genre in genres:
            Genre.objects.create(name=genre['name'], number=genre['id'])

    def get_movies(self):
        if not Genre.objects.count():
            return
        genres = Genre.objects.all()
        for genre in genres:
            MOIVE_URL = f'{self.BASE_URL}/search/movie'
            params = {
                'api_key': self.API_KEY,
                'query': genre.name,
            }
            res = requests.get(MOIVE_URL, params=params)
            movies = res.json()['results']
            for movie in movies:
                genre_ids = movie['genre_ids']
                if movie.get('poster_path'):
                    movie['poster_path'] = f'{self.POSTER_BASE_URL}{movie["poster_path"]}'
                serializer = MovieSerializer(data=movie)
                try:
                    if serializer.is_valid(raise_exception=True):
                        movie = serializer.save()
                    for genre_id in genre_ids:
                        try:
                            genre = Genre.objects.get(number=genre_id)
                            genre.movies.add(movie)
                        except:
                            pass
                except:
                    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        scraper = Scraper()
        scraper.get_genres()
        scraper.get_movies()
