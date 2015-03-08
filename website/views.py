from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from website.forms import UserForm
from django.core.urlresolvers import reverse_lazy, reverse
from ratings.imdb import ImdbPoller, ImdbResponse
from website.models import ImdbUser


class UserView(FormView):
    template_name = 'website/main.html'
    form_class = UserForm
    success_url = reverse_lazy('user-detail')

    def get_success_url(self):
        return reverse('user-detail', kwargs={'user_id': self.user_id})

    def form_valid(self, form):
        user_id = form.cleaned_data['imdb_id']
        self.user_id = user_id
        user = ImdbUser(imdb_id=user_id)
        user.save()
        poller = ImdbPoller('BCYoJE9DlwPgWDsoMxvLpKNRncr8Qi-KgGxbbhgmGnbpOO-shjdGyIyUFboEIltBfpoHWOknFvCJPeKD-ygX9i2URrJ8fsxBFRrvUSxp1V6xTlidhXWPORBqGwDg2GEKM4iUCG28RuRTAsRo0hBqZ52QVzuo9wqwFxFc2J6Ha9n0EYdipmHMrV8_0W2E_gNq6US1')
        response = poller.requestRatingsResponse(user_id)
        if response.status_code == 404:
            user.delete()
            return HttpResponse("Either user does not exist or error querying IMDB")
        imdb_response = ImdbResponse(response)
        imdb_response.addFilmsAndRatingsFromCSV(user)
        return super(UserView, self).form_valid(form)


def user_detail(request, user_id):
    return HttpResponse("Home Page " + user_id)
