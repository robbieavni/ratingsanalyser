from django.contrib import admin
from films.models import Film, Director, Genre

# Register your models here.

class FilmDirectorInLine(admin.StackedInline):
    model = Director.films.through
    extra = 0


class DirectorAdmin(admin.ModelAdmin):
    inlines = [FilmDirectorInLine]
    exclude = ('films',)


class FilmGenreInLine(admin.StackedInline):
    model = Genre.films.through
    extra = 0


class GenreAdmin(admin.ModelAdmin):
    inlines = [FilmGenreInLine]
    exclude = ('films',)

admin.site.register(Film)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Genre, GenreAdmin)
