from django.test import TransactionTestCase
from imdb import ImdbPoller, ImdbResponse
from films.models import Film, Director, Genre
from ratings.models import Rating
from website.models import ImdbUser


class ImdbPollerTestCase(TransactionTestCase):
    def setUp(self):
        self.poller = ImdbPoller('BCYoJE9DlwPgWDsoMxvLpKNRncr8Qi-KgGxbbhgmGnbpOO-shjdGyIyUFboEIltBfpoHWOknFvCJPeKD-ygX9i2URrJ8fsxBFRrvUSxp1V6xTlidhXWPORBqGwDg2GEKM4iUCG28RuRTAsRo0hBqZ52QVzuo9wqwFxFc2J6Ha9n0EYdipmHMrV8_0W2E_gNq6US1')
        self.user_id = 'ur2433136'
        self.response = self.poller.requestRatingsResponse(self.user_id)

    def test_response(self):
        """Able to get a CSV response from IMDB"""
        self.assertEqual(self.response.status_code,200)
        self.assertEqual(self.response.headers._store['content-type'][1],'text/csv; charset=utf-8')

class ImdbParserTestCase(TransactionTestCase):
    def setUp(self):
        self.user_id = 'ur9663707'
        self.response = Object()
        self.response.content = """"position","const","created","modified","description","Title","Title type","Directors","You rated","IMDb Rating","Runtime (mins)","Year","Genres","Num. Votes","Release Date (month/day/year)","URL"
"1","tt2381941","Sun Mar  1 00:00:00 2015","","","Focus","Feature Film","Glenn Ficarra, John Requa","6","7.0","104","2015","comedy, crime, drama, romance","3467","2015-02-25","http://www.imdb.com/title/tt2381941/"
"2","tt1259521","Tue Jan 20 00:00:00 2015","","","The Cabin in the Woods","Feature Film","Drew Goddard","6","7.0","95","2012","horror, mystery, thriller","232730","2012-03-09","http://www.imdb.com/title/tt1259521/"
"3","tt0119094","Sat Jan  3 00:00:00 2015","","","Face/Off","Feature Film","John Woo","7","7.3","138","1997","action, crime, sci_fi, thriller","251390","1997-06-27","http://www.imdb.com/title/tt0119094/\""""

    def test_parse_csv_adding_films_and_ratings(self):
        """Successfully adds films and ratings to database"""
        user = ImdbUser(imdb_id=self.user_id)
        user.save()
        self.imdb_response = ImdbResponse(self.response)
        self.imdb_response.addFilmsAndRatingsFromCSV(user)

        films = Film.objects.all()
        count = len(films)
        self.assertEqual(count, 3)
        ratings = Rating.objects.all()
        self.assertEqual(len(ratings), count)
        directors = Director.objects.all()
        self.assertEqual(len(directors), 4)
        genres = Genre.objects.all()
        self.assertEqual(len(genres), 9)

        cabin = Film.objects.get(imdb_id='tt1259521')
        self.assertEqual(cabin.title, 'The Cabin in the Woods')
        self.assertEqual(cabin.runtime, 95)
        self.assertEqual(cabin.year, 2012)
        cabin_genres = cabin.genre_set.all()
        self.assertEqual(len(cabin_genres), 3)
        self.assertEqual(cabin_genres[0].genre, 'horror')

        focus = Film.objects.get(imdb_id='tt2381941')
        focus_directors = focus.director_set.all()
        self.assertEqual(len(focus_directors), 2)
        self.assertEqual(focus_directors[0].name, 'Glenn Ficarra')

        # Parse a second time and test that no duplicates are added
        self.imdb_response.addFilmsAndRatingsFromCSV(user)
        films = Film.objects.all()
        self.assertEqual(len(films), count)
        ratings = Rating.objects.all()
        self.assertEqual(len(ratings), count)
        directors = Director.objects.all()
        self.assertEqual(len(directors), 4)


class Object(object):
    pass