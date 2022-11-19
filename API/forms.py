from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bracket.models import UsersPoints, Prediction

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","first_name","last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
            points = UsersPoints(owner=user)
            points.save()
        return user