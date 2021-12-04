from django.urls import path
from .views import (
                    ClusterListView,
                    ClusterCreateView,
                    ClusterDetailView,
                    ClusterUpdateView,
                    ClusterDeleteView,
                    ClusterNoteCreateView,
                    NoteCreateView,
                    NoteUpdateView,
                    NoteDetailView,
                    NoteDeleteView,
                    )


app_name="cluster"

urlpatterns = [
    path("",ClusterListView.as_view(),name="clusterlist"),
    path("create/",ClusterCreateView.as_view(),name="clustercreate"),
    path("<slug:code_name>/",ClusterDetailView.as_view(),name="clusterdetail"),
    path("<slug:code_name>/update/",ClusterUpdateView.as_view(),name="clusterupdate"),
    path("<slug:code_name>/delete/",ClusterDeleteView.as_view(),name="clusterdelete"),
    path("note/create/",NoteCreateView.as_view(),name="notecreate"),
    path("<slug:code_name>/note/create/",ClusterNoteCreateView.as_view(),name="clusternotecreates"),
    path("<slug:cluster>/<slug:code>/",NoteDetailView.as_view(),name="notedetail"),
    path("<slug:cluster>/<slug:code>/update/",NoteUpdateView.as_view(),name="noteupdate"),
    path("<slug:cluster>/<slug:code>/delete/",NoteDeleteView.as_view(),name="notedelete"),
    
]
