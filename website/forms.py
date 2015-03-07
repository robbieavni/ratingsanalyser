from django.forms import ModelForm
from website.models import ImdbUser

class UserForm(ModelForm):
    class Meta:
        model = ImdbUser
        fields = ['imdb_id']