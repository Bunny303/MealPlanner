from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^accounts/register/$', views.AccountRegistrationView.as_view(), name='register'),
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.LogoutView.as_view(), name='logout'),
    url('^change-password/', auth_views.password_change,
        {'template_name': 'authentication/change-password.html',
         'post_change_redirect': reverse_lazy('password_change_done')},
        name='password_change'),
    url('^password-change-done/', auth_views.password_change_done, name='password_change_done')
]
