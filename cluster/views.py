from django.core.checks.messages import Error
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, reverse 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ClusterModel, NoteModel
from django.views.generic import (
                                    TemplateView,
                                    ListView,
                                    DetailView,
                                    CreateView,
                                    DeleteView,
                                    UpdateView
                                )  
from .forms import ClusterCreationForm,ClusterUpdateForm, NoteCreationForm, NoteUpdateForm


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
    slug_url_kwarg="code_name"
    slug_field="code_name"

    def get_context_data(self,**kwargs):
        context=super(ClusterDetailView,self).get_context_data(**kwargs)
        notes=self.get_object().NoteModel_ClusterModel.all()              
        context["notes"]=notes
        return context

class ClusterUpdateView(LoginRequiredMixin,UpdateView):
    template_name="cluster/cluster_update.html"
    model=ClusterModel
    form_class=ClusterUpdateForm
    slug_url_kwarg="code_name"
    slug_field="code_name"
    

    def dispatch(self, request, *args, **kwargs):
        cluster=self.get_object()
        if cluster.owner != self.request.user:
            raise Http404("Knock knock , Not you!")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("cluster:clusterlist")


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
        return super(NoteCreateView,self).form_valid(form)

    def get_success_url(self):
        return reverse("cluster:clusterlist")

class NoteDetailView(DetailView):

    model=NoteModel
    template_name="cluster/note_detail.html"
    context_object_name="note"
    
    def get_object(self, queryset=None):
       
        if queryset is None:
            queryset = self.get_queryset()
            

        cluster_slug = self.kwargs.get('cluster', None)
        code_slug = self.kwargs.get('code', None)

        try:
            obj = queryset.get(code=code_slug, cluster__code_name =cluster_slug)
            
        except ObjectDoesNotExist:
            raise Http404(f"Object not found ")

        return obj    
        
        """                      

        cluster_slug = self.kwargs.get('cluster', None)
        code_slug = self.kwargs.get('code', None)
        try:
            obj = NoteModel.objects.get(code=code_slug, cluster__code_name =cluster_slug)        
        except ObjectDoesNotExist: 
            raise Http404(f"Object not found ")
        
        return obj    

         """

class NoteUpdateView(UpdateView):
    template_name="cluster/note_update.html"
    model=NoteModel
    form_class=NoteUpdateForm

    def get_form_kwargs(self,**kwargs):
        kwargs=super(NoteUpdateView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request    
        })
       
        return kwargs
    
    def get_object(self, queryset=None):
       
        if queryset is None:
            queryset = self.get_queryset()
            

        cluster_slug = self.kwargs.get('cluster', None)
        code_slug = self.kwargs.get('code', None)

        try:
            obj = queryset.get(code=code_slug, cluster__code_name =cluster_slug)
            
        except ObjectDoesNotExist:
            raise Http404(f"Object not found ")

        return obj  

    def dispatch(self, request, *args, **kwargs):
        note=self.get_object()
        requesting_user=self.request.user
        if requesting_user != note.author and requesting_user != note.cluster.owner:
            raise Http404("Knock knock , Not you!")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("cluster:clusterlist")

class NoteDeleteView(DeleteView):
    template_name="cluster/note_delete.html"
    #optimization required for queryset
    queryset=NoteModel.objects.all() 
    

    def get_object(self):
               
        cluster_slug = self.kwargs.get('cluster', None)
        code_slug = self.kwargs.get('code', None)

        try:
            obj = NoteModel.objects.get(code=code_slug, cluster__code_name =cluster_slug)
            
        except ObjectDoesNotExist:
            raise Http404(f"Object not found ")
        return obj


    def dispatch(self, request, *args, **kwargs):
        note=self.get_object()
        requesting_user=self.request.user
        if requesting_user != note.author and requesting_user != note.cluster.owner:
            raise Http404("Knock knock , Not you!")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("cluster:clusterlist")      


        
    


