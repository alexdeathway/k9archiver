from django.shortcuts import render
from django.views.generic import TemplateView
from cluster.models import NoteModel,NoteEventModel,ClusterModel

class Home(TemplateView):
    template_name="home.html"

    def get_context_data(self, **kwargs):
        context = super(Home,self).get_context_data(**kwargs)
        context["latest_events"] = NoteEventModel.objects.order_by('-id')[:5]
        return context
    