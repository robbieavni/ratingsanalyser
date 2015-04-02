from django import forms
from website.models import ImdbUser

class UserForm(forms.ModelForm):
    class Meta:
        model = ImdbUser
        fields = ['imdb_id']


class UploadFileForm(forms.Form):
    file = forms.FileField()