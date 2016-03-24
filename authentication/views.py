from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView, FormView
from django.core.urlresolvers import reverse_lazy


class AccountRegistrationView(FormView):
    template_name = 'authentication/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        saved_user = form.save()
        user = authenticate(
            username=saved_user.username,
            password=form.cleaned_data['password1'])
        # cache.clear()
        auth_login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class LoginView(FormView):
    template_name = 'authentication/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        # cache.clear()
        auth_login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, RedirectView):
    permanent = False
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        # cache.clear()
        auth_logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)
