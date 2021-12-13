from django.shortcuts import render,reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView,TemplateView

from django.http import Http404
from cluster.models import NoteModel,ClusterModel
from .forms import CustomUserCreationForm


User=get_user_model()

class UserSignupView(CreateView):
    template_name="registration/signup.html"
    form_class=CustomUserCreationForm

    def get_success_url(self):
        return reverse("home")

class UserProfileView(TemplateView):
    template_name="users/profile.html"
    
    def get_context_data(self,**kwargs):
        username=self.kwargs.get('username',None)
        context=super(UserProfileView,self).get_context_data(**kwargs)
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("User doesnt exists!")    
        notes=NoteModel.objects.filter(author=user)
        organisations=ClusterModel.objects.filter(owner=user)
        context["userprofile"]=user
        context["notes"]=notes
        context["organisations"]=organisations
        return context
    
    
