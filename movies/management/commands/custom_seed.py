from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model
import random
from movies.models import Movie, Article, Comment, SimpleRating, DetailedRating

User = get_user_model()


class UserSeeder():
    def __init__(self, number=50):
        self.seeder = Seed.seeder()
        self.number = number

    def execute(self):
        self.seeder.add_entity(User, self.number, {
            'is_staff': 0,
            'is_superuser': 0,
            'password': lambda x: User.objects.make_random_password(length=100),
        })
        self.seeder.execute()


class SimpleRatingSeeder():
    def __init__(self, number=1000, movies=None, users=None):
        self.seeder = Seed.seeder()
        self.number = number
        self.ratings = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
        self.rating_count = len(self.ratings)
        self.movies = movies or Movie.objects.all()
        self.movie_count = len(self.movies)
        self.users = users or User.objects.all()
        self.user_count = len(self.users)

    def execute(self):
        self.seeder.add_entity(SimpleRating, self.number, {
            'movie': lambda x: self.movies[random.randint(0, self.movie_count - 1)],
            'user': lambda x: self.users[random.randint(0, self.user_count - 1)],
            'rating': lambda x: self.ratings[random.randint(0, self.rating_count - 1)],
        })
        self.seeder.execute()


class DetailedRatingSeeder():
    def __init__(self, number=1000, movies=None, users=None):
        self.seeder = Seed.seeder()
        self.number = number
        self.ratings = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
        self.rating_count = len(self.ratings)
        self.movies = movies or Movie.objects.all()
        self.movie_count = len(self.movies)
        self.users = users or User.objects.all()
        self.user_count = len(self.users)

    def execute(self):
        self.seeder.add_entity(DetailedRating, self.number, {
            'movie': lambda x: self.movies[random.randint(0, self.movie_count - 1)],
            'user': lambda x: self.users[random.randint(0, self.user_count - 1)],
            'originality': lambda x: self.ratings[random.randint(0, self.rating_count - 1)],
            'plot': lambda x: self.ratings[random.randint(0, self.rating_count - 1)],
            'characters': lambda x: self.ratings[random.randint(0, self.rating_count - 1)],
            'cinematography': lambda x: self.ratings[random.randint(0, self.rating_count - 1)],
            'music_score': lambda x: self.ratings[random.randint(0, self.rating_count - 1)],
            'entertainment_value': lambda x: self.ratings[random.randint(0, self.rating_count - 1)],
        })
        self.seeder.execute()


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_seeder = UserSeeder(number=50)
        user_seeder.execute()

        MOVIES = Movie.objects.all()
        USERS = User.objects.all()

        simple_rating_seeder = SimpleRatingSeeder(
            number=1000, movies=MOVIES, users=USERS)
        simple_rating_seeder.execute()

        detailed_rating_seeder = DetailedRatingSeeder(
            number=500, movies=MOVIES, users=USERS)
        detailed_rating_seeder.execute()
