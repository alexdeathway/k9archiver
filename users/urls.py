from django.urls import path
from .views import  UserProfileView, UserProfileUpdateView,UserInviteView
                    

app_name="users"

urlpatterns = [
    path("invite/",UserInviteView.as_view(),name="invite"),
    path("<str:username>/",UserProfileView.as_view(),name="profile"),
    path("<str:username>/update/",UserProfileUpdateView.as_view(),name="profileupdate"),
]
