"""archiver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from users.views import UserSignupView
from .views import Home
from django.contrib.auth.views import (
                                        LoginView,
                                        LogoutView,
                                        PasswordResetView,
                                        PasswordResetDoneView,
                                        PasswordResetConfirmView,
                                        PasswordResetCompleteView,
                                      )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(),name="home"),
    path('users/',include('users.urls',namespace='users')),
    path('cluster/',include('cluster.urls',namespace='cluster')),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('signup/',UserSignupView.as_view(),name="signup"),
    path('summernote/', include('django_summernote.urls')),
    path('reset-password/',PasswordResetView.as_view(),name="reset-password"), 
    path('reset-password-done/',PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset-password-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset-password-complete/',PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')),)
  
