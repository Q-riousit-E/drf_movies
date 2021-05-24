from django.contrib import admin
from .models import Movie, Genre, Article, Comment, SimpleRating, DetailedRating


class MovieAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class SimpleRatingAdmin(admin.ModelAdmin):
    pass


class DetailedRatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SimpleRating, SimpleRatingAdmin)
admin.site.register(DetailedRating, DetailedRatingAdmin)
