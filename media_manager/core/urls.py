from django.conf.urls import url
from django.contrib.auth import logout

from .views import (IndexView, LoginView, LogOutView, 
                   MoodsView, ProfileView, SignupView)


urlpatterns = [
    # for user authentication
    url(r'^login/$', LoginView.as_view(), name="login-view"),
    url(r'^signup/$', SignupView.as_view(), name="signup-view"),
    url(r'^logout/$', LogOutView.as_view(), name="logout-view"),

    url(r'^home/$', IndexView.as_view(), name="home-view"),
    url(r'^profile/$', ProfileView.as_view(), name="profile-view"),
    url(r'^moods/$', MoodsView.as_view(), name="moods-view"),
]
