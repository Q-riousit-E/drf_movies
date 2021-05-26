from requests.api import post
from movies.models import Movie, Genre
from movies.serializers import MovieSerializer
import requests
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


class Scraper:
    BASE_URL = 'https://api.themoviedb.org/3'
    IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/original'
    TRAILER_BASE_URL = 'https://youtube.com/embed'
    API_KEY = os.environ.get('TMDB_API_KEY')

    def get_genres(self):
        if Genre.objects.count():
            return
        GENRE_URL = f'{self.BASE_URL}/genre/movie/list'
        params = {'api_key': self.API_KEY}
        res = requests.get(GENRE_URL, params=params)
        genres = res.json()['genres']
        for genre in genres:
            Genre.objects.create(name=genre['name'], number=genre['id'])

    def get_video_key(self, movie_id):
        VIDEO_URL = f'{self.BASE_URL}/movie/{movie_id}/videos'
        params = {'api_key': self.API_KEY}
        res = requests.get(VIDEO_URL, params=params)
        videos = res.json().get('results')
        for video in videos:
            if video.get('site') == 'YouTube' and video.get('type') == 'Trailer' and video.get('key'):
                return video.get('key')
        return None

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
                movie_id = movie.get('id')
                genre_ids = movie['genre_ids']
                poster_paths = self.get_poster_paths(movie_id)
                if not poster_paths:
                    continue
                for i in range(1, 5):
                    movie[f'poster_path{i}'] = f'{self.IMAGE_BASE_URL}/{poster_paths[i-1]}'
                movie_key = self.get_video_key(movie_id)
                if movie_key:
                    movie['trailer_path'] = f'{self.TRAILER_BASE_URL}/{movie_key}'
                credit_info = self.get_credit_info(movie_id)
                for key, value in credit_info.items():
                    movie[f'{key}'] = value
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

    def get_credit_info(self, movie_id):
        CREDITS_URL = f'{self.BASE_URL}/movie/{movie_id}/credits'
        params = {'api_key': self.API_KEY}
        res = requests.get(CREDITS_URL, params=params)
        data = res.json()
        casts = data.get('cast')
        info = {}
        if len(casts):
            i = 1
            for cast in casts[:3]:
                info[f'cast{i}_name'] = cast.get('name')
                info[f'cast{i}_character'] = cast.get('character')
                i += 1
        crews = data.get('crew')
        for crew in crews:
            if not crew.get('job') == 'Director':
                continue
            info['director_name'] = crew.get('name')
            break

        return info

    def get_poster_paths(self, movie_id):
        POSTERS_URL = f'{self.BASE_URL}/movie/{movie_id}/images'
        params = {'api_key': self.API_KEY}
        res = requests.get(POSTERS_URL, params=params)
        data = res.json()
        posters = data.get('posters')
        if len(posters) < 4:
            return None
        return [poster.get('file_path') for poster in posters[:4]]


class Command(BaseCommand):
    def handle(self, *args, **options):
        scraper = Scraper()
        scraper.get_genres()
        scraper.get_movies()
