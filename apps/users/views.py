from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import  reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.http import HttpResponseRedirect
from .forms import CreateUserForm, ArchitectLoginForm



class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class LoginView(BaseLoginView):
    form_class = ArchitectLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


