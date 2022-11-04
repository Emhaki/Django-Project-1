from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
<<<<<<< HEAD
        fields = ["username", "email",]
=======
        fields = ["username", "email"]
>>>>>>> 0d9780babf1c6df5f6784d53a79289d4e3257d91


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
