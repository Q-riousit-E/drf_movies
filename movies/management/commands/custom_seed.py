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

        self.ratings = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5,
                        4.0, 4.5, 5.0, 3.0, 3.5, 4.0, 4.5, 4.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0)
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

        self.rating_candidate1 = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5,
                                  4.0, 4.5, 5.0, 3.0, 3.5, 4.0, 4.5, 4.0, 4.5, 5.0, 4.5, 5.0)
        self.rating_candidate2 = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5,
                                  4.0, 4.5, 5.0, 3.0, 3.5, 4.0, 4.5, 4.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0)
        self.rating_candidate3 = (
            0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 3.0, 3.5, 4.0, 4.5)
        self.rating_candidate4 = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5,
                                  4.0, 4.5, 5.0, 3.0, 3.5, 4.0, 4.5, 4.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0)
        self.rating_candidate5 = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5,
                                  4.0, 4.5, 5.0, 3.0, 3.5, 4.0, 4.5, 4.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0)
        self.rating_candidate6 = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5,
                                  4.0, 4.5, 5.0, 3.0, 3.5, 4.0, 4.5, 4.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0, 4.5, 5.0)

        self.rating_sets = ((self.rating_candidate1, len(
            self.rating_candidate1) - 1), (self.rating_candidate2, len(self.rating_candidate2) - 1), (self.rating_candidate3, len(self.rating_candidate3) - 1), (self.rating_candidate4, len(self.rating_candidate4) - 1), (self.rating_candidate5, len(self.rating_candidate5) - 1), (self.rating_candidate6, len(self.rating_candidate6) - 1))
        self.rating_sets_upper_idx = len(self.rating_sets) - 1

    def execute(self):
        inserted_pks = [0] * self.number_of_insertions
        for i in range(self.number_of_insertions):
            movie_idx = self.movie_user_idx_combinations[i][0]
            user_idx = self.movie_user_idx_combinations[i][1]
            kwargs = {
                'movie': self.movies[movie_idx],
                'user': self.users[user_idx],
                'originality': None,
                'plot': None,
                'cinematography': None,
                'music_score': None,
                'characters': None,
                'entertainment_value': None,
            }
            criteria = ['originality', 'plot', 'cinematography',
                        'music_score', 'characters', 'entertainment_value']
            for i in range(len(criteria)):
                criterion = criteria[i]
                rating_candidate, candidate_upper_idx = self.rating_sets[i]
                kwargs[criterion] = rating_candidate[random.randint(
                    0, candidate_upper_idx)]

            new_rating = DetailedRating.objects.create(**kwargs)
            inserted_pks[i] = new_rating.pk
        return inserted_pks


class ArticleGenerator():
    def __init__(self, users=None, movies=None):
        self.users = users or User.objects.all()
        self.number_of_users = self.users.count()
        self.movies = movies or Movie.objects.all()
        self.number_of_movies = self.movies.count()
        self.number_of_insertions = self.number_of_movies // 5 * self.number_of_users
        self.contents = ['간만에 좋은 영화였습니다. 추천드려요~', '가족과 함께 보면 좋을 영화!',
                         '예전에 보고 너무 인상 깊어서 다시 봤는데, 그 때는 느끼지 못했던 감성과 메세지를 얻어갑니다. 볼 때마다 감회가 새로운 영화..!',
                         '이런 영화를 여태 안 보고 뭐했는지..!',
                         '역시 믿고 보는 배우...! 믿고 보는 감독...! 최고입니다.',
                         '인생 작품',
                         '개인적으로 너무 좋아하는 영화라서 5번째 보는 중']
        self.number_of_contents = len(self.contents)

    def execute(self):
        nums = [i for i in range(self.number_of_movies)]
        for user in self.users:
            for movie in random.sample(list(self.movies), self.number_of_movies // 5):
                article = Article.objects.create(
                    user=user, movie=movie, content=self.contents[random.randint(0, self.number_of_contents - 1)])


class CommentGenerator():
    def __init__(self, users=None, articles=None):
        self.users = users or User.objects.all()
        self.number_of_users = self.users.count()
        self.articles = articles or Article.objects.all()
        self.number_of_articles = self.articles.count()
        self.number_of_insertions = self.number_of_articles // 10 * self.number_of_users
        self.contents = [
            '동감..!', '저랑 취향이 비슷하신 듯!!', '오.. 저도 같은 생각이에요', '22222222', 'ㅇㅇ 간만에 괜찮은 영화 발견', '한 번 봐야겠네요!']
        self.number_of_contents = len(self.contents)

    def execute(self):
        nums = [i for i in range(self.number_of_articles)]
        for user in self.users:
            for article in random.sample(list(self.articles), self.number_of_articles // 100):
                article = Comment.objects.create(
                    user=user, article=article, content=self.contents[random.randint(0, self.number_of_contents - 1)])


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_seeder = UserSeeder(number=100)
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
                                                            max_number=(len(INSERTED_USERS)*len(MOVIES))//10, movies=MOVIES)
        detailed_rating_generator.execute()
        article_generator = ArticleGenerator()
        article_generator.execute()
        comment_generator = CommentGenerator()
        comment_generator.execute()
