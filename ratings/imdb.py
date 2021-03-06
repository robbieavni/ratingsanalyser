import requests
import StringIO
import csv
import datetime
from films.models import Film, Director, Genre
from ratings.models import Rating

class ImdbPoller():

    def __init__(self, cookie='BCYoJE9DlwPgWDsoMxvLpKNRncr8Qi-KgGxbbhgmGnbpOO-shjdGyIyUFboEIltBfpoHWOknFvCJPeKD-ygX9i2URrJ8fsxBFRrvUSxp1V6xTlidhXWPORBqGwDg2GEKM4iUCG28RuRTAsRo0hBqZ52QVzuo9wqwFxFc2J6Ha9n0EYdipmHMrV8_0W2E_gNq6US1'):
        self.headers = {'cookie': 'id=' + cookie}

    def requestRatingsResponse(self, author_id):
        payload = {'list_id': 'ratings', 'author_id': author_id}
        response = requests.get('http://www.imdb.com/list/export', params=payload, headers=self.headers)
        return response


class ImdbResponse():

    def __init__(self, response):
        self.response = response

    def addFilmsAndRatingsFromResponse(self, user):
        ratings_list = StringIO.StringIO(self.response.content)
        reader = csv.DictReader(ratings_list, delimiter=',')
        addFilmsAndRatingsFromCSV(user, reader)


def addFilmsAndRatingsFromCSV(user, reader):
    name = reader.fieldnames[8].split(' ')[0]

    for row in reader:
        this_film = addFilm(row)
        if this_film:
            this_rating = addRating(user, this_film, name, row)

def addFilm(row):
    type = next(value for value, name in Film.FILM_TYPE_CHOICES if name==row['Title type'])
    if type not in {'FF','D','V','TVM'}:
        return False

    if len(row['Release Date (month/day/year)'].split('-')) == 2:
        released = datetime.datetime.strptime(row['Release Date (month/day/year)'], "%Y-%m")
    else:
        released = datetime.datetime.strptime(row['Release Date (month/day/year)'], "%Y-%m-%d")

    if (row['IMDb Rating'] == ''):
        return False

    values = {'title': row['Title'], 'type': type, 'year': row['Year'], 'runtime': int(row['Runtime (mins)']),
                        'released': released, 'imdb_rating': float(row['IMDb Rating']),
                        'number_of_votes': int(row['Num. Votes'])}

    film, created = Film.objects.update_or_create(imdb_id=row['const'], defaults=values )

    addDirectors(film, row['Directors'])
    addGenres(film, row['Genres'])

    return film

def addRating(user, film, name, row):
    date_rated = datetime.datetime.strptime(row['created'], "%a %b %d %X %Y")
    this_rating, created = Rating.objects.get_or_create(user=user, rating=row[name + ' rated'],
                                            date_rated=date_rated, film=film)

def addDirectors(film, directors_field):
    directors = [x.strip() for x in directors_field.split(',')]
    for director in directors:
        this_director, created = Director.objects.get_or_create(name=director)
        this_director.films.add(film)

def addGenres(film, genre_field):
    genres = [x.strip().replace('_','-') for x in genre_field.split(',')]
    for genre in genres:
        this_genre, created = Genre.objects.get_or_create(genre=genre)
        this_genre.films.add(film)