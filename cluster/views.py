from django.shortcuts import render, reverse 
from .models import ClusterModel
from django.views.generic import (
                                    TemplateView,
                                    ListView,
                                    DetailView,
                                    CreateView
                                )  
from django.views.generic.edit import UpdateView
# Create your views here.

class ModelCreateView(CreateView):
    pass


class ClusterListView(ListView):
    template_name = "cluster/cluster_list.html"
    context_object_name="cluster"
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

        
    


