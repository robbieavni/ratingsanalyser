import requests
import StringIO
import csv
import datetime
from films.models import Film
from ratings.models import Rating

class ImdbPoller():

    def __init__(self, cookie):
        self.headers = {'cookie': 'id=' + cookie}

    def requestRatingsResponse(self, author_id):
        payload = {'list_id': 'ratings', 'author_id': author_id}
        response = requests.get('http://www.imdb.com/list/export', params=payload, headers=self.headers)
        return response


class ImdbResponse():

    def __init__(self, response):
        self.response = response

    def addFilmsAndRatingsFromCSV(self, user_id):
        ratings_list = StringIO.StringIO(self.response.content)
        reader = csv.DictReader(ratings_list, delimiter=',')
        name = reader.fieldnames[8].split(' ')[0]
        for row in reader:
            this_film = self.addFilm(row)
            this_rating = self.addRating(user_id, this_film, name, row)

    def addFilm(self, row):
        type = next(value for value, name in Film.FILM_TYPE_CHOICES if name==row['Title type'])
        if len(row['Release Date (month/day/year)'].split('-')) == 2:
            released = datetime.datetime.strptime(row['Release Date (month/day/year)'], "%Y-%m")
        else:
            released = datetime.datetime.strptime(row['Release Date (month/day/year)'], "%Y-%m-%d")
        # TODO Only create if doesn't exist yet in database
        return Film.objects.create(imdb_id=row['const'], title=row['Title'], type=type, year=row['Year'],
                            runtime=int(row['Runtime (mins)']), released=released, imdb_rating=float(row['IMDb Rating']),
                            number_of_votes=int(row['Num. Votes']))

    def addRating(self, user_id, film, name, row):
        date_rated = datetime.datetime.strptime(row['created'], "%a %b %d %X %Y")
        this_rating = Rating.objects.create(user_id=user_id, rating=row[name + ' rated'],
                                                date_rated=date_rated, film=film)