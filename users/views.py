from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView,TemplateView,UpdateView

from django.http import Http404
from cluster.models import NoteModel,ClusterModel,NoteEventModel
from .forms import CustomUserCreationForm,UserUpdateForm


User=get_user_model()

class UserSignupView(CreateView):
    template_name="registration/signup.html"
    form_class=CustomUserCreationForm

    def form_valid(self,form):
        
        return super().form_valid(form)

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
        clusters=ClusterModel.objects.filter(owner=user)
        context["userprofile"]=user
        context["notes"]=notes
        context["clusters"]=clusters
        context["contributions"]=NoteEventModel.objects.filter(event_by=user)
        return context

class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
    template_name="users/user_update.html"
    #form_class=UserUpdateForm
    model=User
    form_class=UserUpdateForm
    slug_url_kwarg="username"
    slug_field="username"
    
    def dispatch(self, request, *args, **kwargs):
        profile=self.get_object()
        if profile != self.request.user:
            raise Http404("Knock knock , Not you!")
        return super().dispatch(request, *args, **kwargs)
    

    def get_success_url(self):
        return reverse("home")

class EmailVerificationView():
    pass

    
    
