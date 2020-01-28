from django.conf.urls import url
from django.contrib.auth import logout

from .views import (IndexView, LoginView, LogOutView, SignupView)

# app_name = 'core'


urlpatterns = [
    # for user authentication
    url(r'^login/$', LoginView.as_view(), name="login-view"),
    url(r'^signup/$', SignupView.as_view(), name="signup-view"),
    url(r'^logout/$', LogOutView.as_view(), name="logout-view"),

    url(r'^home/$', IndexView.as_view(), name="index-view"),
]
