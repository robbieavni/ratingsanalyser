import requests

class ImdbPoller():

    def __init__(self, cookie):
        self.headers = {'cookie': 'id=' + cookie}

    def requestRatingsResponse(self, author_id):
        payload = {'list_id': 'ratings', 'author_id': author_id}
        response = requests.get('http://www.imdb.com/list/export', params=payload, headers=self.headers)
        return response