from django.shortcuts import render,reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


User=get_user_model()

class UserSignupView(CreateView):
    template_name="registration/signup.html"
    form_class=CustomUserCreationForm

    def get_success_url(self):
        return reverse("home")
