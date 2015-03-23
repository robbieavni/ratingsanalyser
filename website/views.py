from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from ratings.models import Rating
from website.models import ImdbUser


class UserCreateView(CreateView):
    model = ImdbUser
    fields = ['imdb_id']

    def get_success_url(self):
        return reverse('user-detail', kwargs={'pk': self.user_id})

    def form_invalid(self, form):
        self.user_id = form.instance.imdb_id
        if form.instance.process_ratings():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponse("Either user doesn't exist or error querying IMDB")

    def form_valid(self, form):
        user_id = form.cleaned_data['imdb_id']
        self.user_id = user_id
        user, created = ImdbUser.objects.get_or_create(imdb_id=user_id)
        if user.process_ratings():
            return super(UserCreateView, self).form_valid(form)
        else:
            return HttpResponse("Either user doesn't exist or error querying IMDB")


class UserDetailView(DetailView):
    model = ImdbUser

    def get_context_data(self, **kwargs):
        total_rated = Rating.objects.total_for_user(self.object)
        actual_films_rated = Rating.objects.actual_films_rated(self.object)
        average_rating = Rating.objects.average_for_user(self.object)
        average_imdb_rating = Rating.objects.imdb_average_for_users_films(self.object)
        decades_dictionary = Rating.objects.decade_breakdown(self.object)
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['total_rated'] = total_rated
        context['total_films_rated'] = actual_films_rated
        context['average_rating'] = average_rating
        context['average_imdb_rating'] = average_imdb_rating
        context['decades_dictionary'] = decades_dictionary
        return context
