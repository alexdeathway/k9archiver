from django.urls import path
from .views import (
                    ClusterListView,
                    ClusterCreateView,
                    NoteCreateView,
                    )


app_name="cluster"

urlpatterns = [
    path("",ClusterListView.as_view(),name="clusterlist"),
    path("create/",ClusterCreateView.as_view(),name="clustercreate"),
    path("note/create/",NoteCreateView.as_view(),name="notecreate"),
]
