from django.urls import path
from .views import ClusterListView


app_name="cluster"

urlpatterns = [
    path("",ClusterListView.as_view(),name="clusterlist")
]
