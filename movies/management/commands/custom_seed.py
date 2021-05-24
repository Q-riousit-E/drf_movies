from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model
import random
from itertools import combinations, permutations
from movies.models import Movie, Article, Comment, SimpleRating, DetailedRating

User = get_user_model()


class UserSeeder():
    def __init__(self, number=100):
        self.seeder = Seed.seeder()
        self.number = number

    def execute(self):
        self.seeder.add_entity(User, self.number, {
            'is_staff': 0,
            'is_superuser': 0,
            'password': lambda x: User.objects.make_random_password(length=100),
        })
        return self.seeder.execute()


class SimpleRatingGenerator():
    def __init__(self, users, movie_user_idx_combinations, max_number=1000, movies=None):
        self.users = users or User.objects.all()

        self.movie_user_idx_combinations = movie_user_idx_combinations
        self.combination_length = len(self.movie_user_idx_combinations)

        self.number_of_insertions = max_number
        if self.number_of_insertions > self.combination_length:
            self.number_of_insertions = self.combination_length

        self.movie_user_idx_combinations = random.sample(
            self.movie_user_idx_combinations, self.number_of_insertions)

        self.movies = movies or Movie.objects.all()

        self.ratings = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
        self.ratings_upper_idx = len(self.ratings) - 1

    def execute(self):
        inserted_pks = [0] * self.number_of_insertions
        for i in range(self.number_of_insertions):
            movie_idx = self.movie_user_idx_combinations[i][0]
            user_idx = self.movie_user_idx_combinations[i][1]
            kwargs = {
                'movie': self.movies[movie_idx],
                'user': self.users[user_idx],
                'rating': self.ratings[random.randint(0, self.ratings_upper_idx)],
            }
            new_rating = SimpleRating.objects.create(**kwargs)
            inserted_pks[i] = new_rating.pk
        return inserted_pks


class DetailedRatingGenerator():
    def __init__(self, users, movie_user_idx_combinations, max_number=1000, movies=None):
        self.users = users or User.objects.all()

        self.movie_user_idx_combinations = movie_user_idx_combinations
        self.combination_length = len(self.movie_user_idx_combinations)

        self.number_of_insertions = max_number
        if self.number_of_insertions > self.combination_length:
            self.number_of_insertions = self.combination_length

        self.movie_user_idx_combinations = random.sample(
            self.movie_user_idx_combinations, self.number_of_insertions)

        self.movies = movies or Movie.objects.all()

        self.ratings = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
        self.ratings_upper_idx = len(self.ratings) - 1

    def execute(self):
        inserted_pks = [0] * self.number_of_insertions
        for i in range(self.number_of_insertions):
            movie_idx = self.movie_user_idx_combinations[i][0]
            user_idx = self.movie_user_idx_combinations[i][1]
            kwargs = {
                'movie': self.movies[movie_idx],
                'user': self.users[user_idx],
                'originality': self.ratings[random.randint(0, self.ratings_upper_idx)],
                'plot': self.ratings[random.randint(0, self.ratings_upper_idx)],
                'cinematography': self.ratings[random.randint(0, self.ratings_upper_idx)],
                'music_score': self.ratings[random.randint(0, self.ratings_upper_idx)],
                'characters': self.ratings[random.randint(0, self.ratings_upper_idx)],
                'entertainment_value': self.ratings[random.randint(0, self.ratings_upper_idx)],
            }
            new_rating = DetailedRating.objects.create(**kwargs)
            inserted_pks[i] = new_rating.pk
        return inserted_pks


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_seeder = UserSeeder(number=50)
        INSERTED_USER_PKS = list(user_seeder.execute().values())[0]
        INSERTED_USERS = [User.objects.get(
            pk=INSERTED_USER_PKS[i]) for i in range(len(INSERTED_USER_PKS))]

        MOVIES = Movie.objects.all()
        MOVIE_USER_IDX_COMBINATIONS = [(i, j) for i in range(
            len(MOVIES)) for j in range(len(INSERTED_USERS))]
        simple_rating_generator = SimpleRatingGenerator(users=INSERTED_USERS, movie_user_idx_combinations=MOVIE_USER_IDX_COMBINATIONS,
                                                        max_number=len(INSERTED_USERS)*len(MOVIES), movies=MOVIES)
        simple_rating_generator.execute()

        detailed_rating_generator = DetailedRatingGenerator(users=INSERTED_USERS, movie_user_idx_combinations=MOVIE_USER_IDX_COMBINATIONS,
                                                            max_number=len(INSERTED_USERS)*len(MOVIES), movies=MOVIES)
        detailed_rating_generator.execute()
