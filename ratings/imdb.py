import requests
import StringIO
import csv
import datetime
from films.models import Film, Director
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

    def addFilmsAndRatingsFromCSV(self, user):
        ratings_list = StringIO.StringIO(self.response.content)
        reader = csv.DictReader(ratings_list, delimiter=',')
        name = reader.fieldnames[8].split(' ')[0]

        for row in reader:
            this_film = self.addFilm(row)
            if this_film:
                this_rating = self.addRating(user, this_film, name, row)

    def addFilm(self, row):
        type = next(value for value, name in Film.FILM_TYPE_CHOICES if name==row['Title type'])
        if type not in {'FF','D','V','TVM'}:
            return False

        if len(row['Release Date (month/day/year)'].split('-')) == 2:
            released = datetime.datetime.strptime(row['Release Date (month/day/year)'], "%Y-%m")
        else:
            released = datetime.datetime.strptime(row['Release Date (month/day/year)'], "%Y-%m-%d")

        values = {'title': row['Title'], 'type': type, 'year': row['Year'], 'runtime': int(row['Runtime (mins)']),
                            'released': released, 'imdb_rating': float(row['IMDb Rating']),
                            'number_of_votes': int(row['Num. Votes'])}

        film, created = Film.objects.update_or_create(imdb_id=row['const'], defaults=values )

        self.addDirectors(film, row['Directors'])

        return film

    def addRating(self, user, film, name, row):
        date_rated = datetime.datetime.strptime(row['created'], "%a %b %d %X %Y")
        this_rating, created = Rating.objects.get_or_create(user=user, rating=row[name + ' rated'],
                                                date_rated=date_rated, film=film)

    def addDirectors(self, film, directors_field):
        directors = [x.strip() for x in directors_field.split(',')]
        for director in directors:
            this_director, created = Director.objects.get_or_create(name=director)
            this_director.films.add(film)
