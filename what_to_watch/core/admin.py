from django.contrib import admin

# Register your models here.
from django.template.defaultfilters import slugify
from django.utils.html import format_html

from core.models import Movie



class MovieAdmin(admin.ModelAdmin):
    """
    Movie admin.
    """
    list_display = ('movie_title', 'rating', 'votes', 'release_year', 'genre')
    readonly_fields = list_display
    ordering = ('-rating', '-votes')
    search_fields = ('title', 'rating', 'release_year', 'genre')
    advanced_filter_fields = ('title')
    change_list_template = 'admin/movie_summary_change_list.html'

    def movie_title(self, movie):
        title = slugify(movie.title)
        link = "<a href=https://www.youtube.com/results?search_query={}-movie-trailer>{}</a>".format(title, movie.title)
        print(link)
        return format_html(link)

admin.site.register(Movie, MovieAdmin)
