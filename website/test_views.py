from django.test import TestCase, TransactionTestCase
from django.core.urlresolvers import reverse


class UserDetailViewTests(TestCase):
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


class UserCreateViewTests(TestCase):

    def test_create_no_user(self):
        create_url = reverse("user-create")
        post_data = {"imdb_id": "ur9999999"}
        response = self.client.post(create_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context)

    def test_create_real_user(self):
        create_url = reverse("user-create")
        post_data = {"imdb_id": "ur1534810"}
        response = self.client.post(create_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertTrue('average_imdb_rating' in response.context)