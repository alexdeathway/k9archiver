from django.http import Http404
from django.shortcuts import render, reverse 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ClusterModel, NoteModel
from django.views.generic import (
                                    TemplateView,
                                    ListView,
                                    DetailView,
                                    CreateView
                                )  
from django.views.generic.edit import UpdateView
from .forms import ClusterCreationForm, NoteCreationForm, NoteUpdateForm
# Create your views here.

class ClusterCreateView(LoginRequiredMixin,CreateView):
    template_name="cluster/cluster_create.html"
    form_class=ClusterCreationForm
    
    def form_valid(self,form):
        cluster = form.save(commit=False)
        cluster.owner = self.request.user
        cluster.save()

        return super(ClusterCreateView,self).form_valid(form)

    def get_success_url(self):
        return reverse("cluster:clusterlist")

class ClusterListView(ListView):
    template_name = "cluster/cluster_list.html"
    context_object_name="clusters"
    queryset=ClusterModel.objects.all()

class ClusterDetailView(DetailView):
    model=ClusterModel
    template_name="cluster/cluster_detail.html"
    context_object_name="cluster"

    def get_context_data(self,**kwargs):
        context=super(ClusterDetailView,self).get_context_data(**kwargs)
        notes=self.get_object().NoteModel_ClusterModel.all()              
        context["notes"]=notes
        return context

class NoteCreateView(LoginRequiredMixin,CreateView):

    template_name="cluster/note_create.html"
    form_class=NoteCreationForm


    def get_form_kwargs(self,**kwargs):
        kwargs=super(NoteCreateView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs
    
    
    def form_valid(self,form):
        note = form.save(commit=False)
        note.author = self.request.user
        note.save()
        return super(ClusterCreateView,self).form_valid(form)

    def get_success_url(self):
        return reverse("cluster:clusterlist")

class NoteDetailView(DetailView):

    model=NoteModel
    template_name="cluster/note_detail.html"
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        cluster_slug = self.kwargs.get('cluster', None)
        note_slug = self.kwargs.get('note', None)
        try:
            obj = queryset.objects.get(title=note_slug, cluster=cluster_slug)
        except queryset.model.DoesNotExist:
            raise Http404("Object not found")
        return obj    

    pass

class NoteUpdateView(UpdateView):
    template_name="cluster/note_update.html"
    model=NoteModel
    form_class=NoteUpdateForm
    slug_url_kwarg="title"
    slug_field="title"
    

    def dispatch(self, request, *args, **kwargs):
        note=self.get_object()
        if note.author != self.request.user:
            raise Http404("Knock knock , Not you!")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("clusterlist")
        
    


