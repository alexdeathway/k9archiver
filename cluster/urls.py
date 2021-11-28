from django.urls import path
from .views import (
                    ClusterListView,
                    ClusterCreateView,
                    ClusterDetailView,
                    ClusterUpdateView,
                    NoteCreateView,
                    NoteUpdateView,
                    NoteDetailView,
                    )


app_name="cluster"

urlpatterns = [
    path("",ClusterListView.as_view(),name="clusterlist"),
    path("create/",ClusterCreateView.as_view(),name="clustercreate"),
    path("<slug:code_name>/",ClusterDetailView.as_view(),name="clusterdetail"),
    path("<slug:code_name>/update/",ClusterUpdateView.as_view(),name="clusterupdate"),
    path("note/create/",NoteCreateView.as_view(),name="notecreate"),
    path("<slug:cluster>/<slug:code>/",NoteDetailView.as_view(),name="notedetail"),
    
]
