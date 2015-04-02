from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from ratings.models import Rating
from website.models import ImdbUser
from website import forms
import csv
import random
import string


class UserCreateView(CreateView):
    model = ImdbUser
    fields = ['imdb_id']

    def get_success_url(self):
        return reverse('website:user-detail', kwargs={'pk': self.user_id})

    def form_invalid(self, form):
        """User id already exists but let's process ratings again so everything is up to date"""
        self.user_id = form.instance.imdb_id
        if form.instance.process_ratings_from_imdb():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponse("Either user doesn't exist or error querying IMDB")

    def form_valid(self, form):
        user_id = form.cleaned_data['imdb_id']
        self.user_id = user_id
        user, created = ImdbUser.objects.get_or_create(imdb_id=user_id)
        if user.process_ratings_from_imdb():
            return super(UserCreateView, self).form_valid(form)
        else:
            return HttpResponse("Either user doesn't exist or error querying IMDB")


class UserCsvView(FormView):
    template_name = 'website/imdbuser_csv_upload.html'
    form_class = forms.UploadFileForm

    def get_success_url(self):
        return reverse('website:user-detail', kwargs={'pk': self.user_id})

    def form_valid(self, form):
        if (form.files.get('file').content_type == 'text/csv'):
            random_string = (''.join(random.choice(string.digits) for i in range(12)))
            self.user_id = "anon" + random_string
            user, created = ImdbUser.objects.get_or_create(imdb_id=self.user_id)
            reader = csv.DictReader(form.files.get('file'))
            user.process_ratings_from_csv(reader)
            return super(UserCsvView,self).form_valid(form)
        else:
            return HttpResponse("Format must be CSV")


class UserDetailView(DetailView):
    model = ImdbUser

    def get_context_data(self, **kwargs):
        total_rated = Rating.objects.total_for_user(self.object)
        actual_films_rated = Rating.objects.actual_films_rated(self.object)
        average_rating = Rating.objects.average_for_user(self.object)
        average_imdb_rating = Rating.objects.imdb_average_for_users_films(self.object)
        decades_dictionary = Rating.objects.decade_breakdown(self.object)
        hipster_list = Rating.objects.hipster_films(self.object)
        runtime_list = Rating.objects.high_low_runtime_list(self.object)
        director_list = Rating.objects.most_watched_directors(self.object)
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['total_rated'] = total_rated
        context['total_films_rated'] = actual_films_rated
        context['average_rating'] = average_rating
        context['average_imdb_rating'] = average_imdb_rating
        context['decades_dictionary'] = sorted(decades_dictionary.iteritems())
        context['hipster_list'] = hipster_list
        context['runtime_list'] = runtime_list
        return context


class UserListView(ListView):
    model = ImdbUser
