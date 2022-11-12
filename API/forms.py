from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bracket.models import UsersPoints


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
            points = UsersPoints(owner=user)
            points.save()
        return user