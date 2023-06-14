from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

from maintenance.mixins import TitleMixin, SuccessUrlMixin


class LoginUser(TitleMixin, SuccessUrlMixin, LoginView):
    template_name = 'maintenance/login.html'
    redirect_authenticated_user = True
    title = 'Авторизация'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
