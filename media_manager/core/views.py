import json

from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (render, render_to_response)
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import (RedirectView, TemplateView, FormView)

from core.backends import EmailModelBackend

from .forms import LoginForm, SignUpForm
from .mixins import LoggedInUserRedirectMixin

# Create your views here.


def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    response = HttpResponse(data, **response_kwargs)
    return response


class LoginView(LoggedInUserRedirectMixin, FormView):
    """
    This view handles authentication of the user, when they first time logs in
    redirects them to login page if not authenticated.
    """
    form_class = LoginForm
    template_name = 'frontend/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        email = form.data['email']
        password = form.data['password']
        if not form.is_valid():
            return render_to_response(
                self.template_name,
                {
                    'form': form, "csrf_token": form.data['csrfmiddlewaretoken'],
                    'email': email
                }
            )
        user_auth = EmailModelBackend()
        user = user_auth.authenticate(username=email, password=password)

        if user:
            login(self.request, user)
            if "next" in self.request.GET:
                url = self.request.GET["next"]
                response = HttpResponseRedirect(url)
                return response
            else:
                response = HttpResponseRedirect('/home')
                return response
        else:
            logout(self.request)
            form._errors["password"] = ["User doesn't exists."]
            return render_to_response(
                self.template_name,
                {
                    'form': form, 'email': email,
                    "csrf_token": form.data['csrfmiddlewaretoken']
                }
            )


class SignupView(LoggedInUserRedirectMixin, FormView):
    """
    This view signs up new user and validates the form on the server side
    """

    form_class = SignUpForm
    template_name = 'frontend/sign-up.html'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        email = form.data['email']
        if not form.is_valid():
            context = {
                'form': form, "csrf_token": form.data['csrfmiddlewaretoken'],
                'email': email
            }
            return render(
                request, context=context, template_name=self.template_name)
        else:
            form.save()
            password = form.data['email']
            user_auth = EmailModelBackend()
            user = user_auth.authenticate(username=email, password=password)
            login(self.request, user)
            return HttpResponseRedirect(reverse('index-view'))


class LogOutView(RedirectView):
    """
    logout view
    """

    def get_redirect_url(self):
        url = reverse("login-view")
        logout(self.request)
        return url


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Home view for user after redirection
    """

    template_name = 'frontend/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context
