from django.urls import path
from .views import UserProfileView

app_name="users"

urlpatterns = [
    path("<str:username>/",UserProfileView.as_view(),name="profile")
]
