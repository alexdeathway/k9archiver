from django.shortcuts import render
from django.views.generic import TemplateView
from cluster.models import NoteModel,NoteEventModel,ClusterModel,CliffNoteModel
from django.db.models import Count

class Home(TemplateView):
    template_name="home.html"

    def get_context_data(self, **kwargs):
        context = super(Home,self).get_context_data(**kwargs)
        context["latest_events"] = NoteEventModel.objects.order_by('-id')[:5]
        context["latest_notes"] = NoteModel.objects.order_by('-id')[:6]
        context["latest_cliffnotes"] = CliffNoteModel.objects.filter(pinned=False).order_by('-id')[:3]
        context["pinned_cliffnotes"]=CliffNoteModel.objects.filter(pinned=True)[:3]
        context["most_active_clusters"] = ClusterModel.objects.annotate(
            event_model_count = Count('NoteModel_ClusterModel')).order_by('-event_model_count')[:3]
        return context
    
