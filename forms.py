from django import forms

from url_shortener.models import URLModel, User


class URLForm(forms.ModelForm):
    class Meta:
        model = URLModel
        exclude = ['id', 'timestamp', 'shortened_url', 'is404', 'original_url', 'user', 'userGenerated', 'url_title']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'timestamp', 'name', 'email']
