from django.contrib import admin
from films.models import Film, Director

# Register your models here.

class FilmDirectorInLine(admin.StackedInline):
    model = Director.films.through
    extra = 0


class DirectorAdmin(admin.ModelAdmin):
    inlines = [FilmDirectorInLine]
    exclude = ('films',)

admin.site.register(Film)
admin.site.register(Director, DirectorAdmin)
