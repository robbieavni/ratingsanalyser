from django.test import TestCase
from django.core.urlresolvers import reverse


class UserViewTests(TestCase):
    fixtures = ['me.json']

    def test_details(self):
        details_url = reverse("user-detail", kwargs={"pk":"ur9663707"})
        response = self.client.get(details_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['average_imdb_rating'],7.63846)

    def test_details_no_user(self):
        details_url = reverse("user-detail", kwargs={"pk":"ur9999999"})
        response = self.client.get(details_url)
        self.assertEqual(response.status_code, 404)