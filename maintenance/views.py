from typing import Any, Optional
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from maintenance.mixins import TitleMixin, SuccessUrlMixin
from maintenance.models import Vehicle, Work, Event, MileageEvent


class LoginUser(TitleMixin, SuccessUrlMixin, LoginView):
    template_name = 'maintenance/login.html'
    redirect_authenticated_user = True
    title = 'Authorization'


class VehicleCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    model = Vehicle
    fields = [
        'vehicle_manufacturer', 'vehicle_model', 'vehicle_body',
        'vehicle_year', 'vehicle_mileage', 'vin_code',
    ]
    title = 'Add new vehicle'


class VehicleEditView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                      UpdateView):
    model = Vehicle
    fields = [
        'vehicle_manufacturer', 'vehicle_model', 'vehicle_body',
        'vehicle_year', 'vin_code',
    ]
    title = 'Edit vehicle data'


class VehicleDeleteView(LoginRequiredMixin, SuccessUrlMixin, TitleMixin,
                        DeleteView):
    model = Vehicle
    title = 'Vehicle deletion'


class VehicleListView(LoginRequiredMixin, TitleMixin, ListView):
    model = Vehicle
    title = 'Vehicle list'
    

class VehicleDetailView(LoginRequiredMixin, TitleMixin, DetailView):
    model = Vehicle
    title = 'Vehicle detail'

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Vehicle:
        return get_object_or_404(Vehicle, vin_code=self.kwargs['vin_code'])


class WorkCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    model = Work
    fields = ['work_type', 'title', 'interval_month', 'interval_km']
    title = 'Add new work'


class WorkEditView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                      UpdateView):
    model = Work
    fields = ['work_type', 'title', 'interval_month', 'interval_km']
    title = 'Edit work data'


class WorkDeleteView(LoginRequiredMixin, SuccessUrlMixin, TitleMixin,
                        DeleteView):
    model = Work
    title = 'Work deletion'


class WorkListView(LoginRequiredMixin, TitleMixin, ListView):
    model = Work
    title = 'List of works'


class WorkDetailView(LoginRequiredMixin, TitleMixin, DetailView):
    model = Work
    title = 'Work detail'
