from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']