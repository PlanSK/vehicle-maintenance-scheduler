from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone

from maintenance.mixins import TitleMixin, SuccessUrlMixin
from maintenance.models import Vehicle, Work, Event, MileageEvent
from maintenance.forms import (EventForm, MileageEventForm, VehicleForm,
                               WorkForm)
from maintenance.services.maintenance import get_maintenance_limits, get_outdate_mileage_level


class LoginUser(TitleMixin, SuccessUrlMixin, LoginView):
    template_name = 'maintenance/login.html'
    redirect_authenticated_user = True
    title = 'Authorization'


class VehicleCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    title = 'Add new vehicle'

    def get_initial(self):
        return {
            'owner': self.request.user,
        }


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

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user)


class VehicleDetailView(LoginRequiredMixin, TitleMixin, DetailView):
    model = Vehicle
    title = 'Vehicle details'

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Vehicle:
        return get_object_or_404(Vehicle, vin_code=self.kwargs['vin_code'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'planed_works': get_maintenance_limits(self.object.vin_code),
            'outdate_mileage_level': get_outdate_mileage_level(self.object.vin_code),
        })
        return context


class WorkCreateView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                     CreateView):
    model = Work
    form_class = WorkForm
    title = 'Add new work'

    def get_initial(self):
        vehicle = get_object_or_404(Vehicle, vin_code=self.kwargs['vin_code'])
        return {
            'vehicle': vehicle,
        }


class WorkEditView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                      UpdateView):
    model = Work
    form_class = WorkForm
    title = 'Edit work data'


class WorkDeleteView(LoginRequiredMixin, SuccessUrlMixin, TitleMixin,
                        DeleteView):
    model = Work
    title = 'Work deletion'


class WorkListView(LoginRequiredMixin, TitleMixin, ListView):
    model = Work
    title = 'List of works'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            vehicle__vin_code=self.kwargs['vin_code'])


class WorkDetailView(LoginRequiredMixin, TitleMixin, DetailView):
    model = Work
    title = 'Work details'


class EventCreateView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                      CreateView):
    model = Event
    form_class = EventForm
    title = 'Add new event'

    def get_initial(self):
        vehicle = get_object_or_404(Vehicle, vin_code=self.kwargs['vin_code'])
        return {
            'vehicle': vehicle,
            'work_date': timezone.now().strftime('%Y-%m-%d'),
            'mileage': vehicle.vehicle_mileage,
        }


class EventEditView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                      UpdateView):
    model = Event
    fields = ['vehicle', 'work_date', 'mileage', 'work', 'part_price',
              'work_price', 'note']
    title = 'Edit event data'


class EventDeleteView(LoginRequiredMixin, SuccessUrlMixin, TitleMixin,
                        DeleteView):
    model = Event
    title = 'Event deletion'


class EventListView(LoginRequiredMixin, TitleMixin, ListView):
    model = Event
    title = 'Events list'


class EventListByTypeView(LoginRequiredMixin, TitleMixin, ListView):
    model = Event
    title = 'Events list'
    template_name = 'maintenance/event_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            work__pk=self.kwargs.get('pk'))


class EventDetailView(LoginRequiredMixin, TitleMixin, DetailView):
    model = Event
    title = 'Event details'


class MileageCreateView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                        CreateView):
    model = MileageEvent
    form_class = MileageEventForm
    title = 'Add new mileage event'
    
    def get_initial(self):
        vehicle = get_object_or_404(Vehicle, vin_code=self.kwargs['vin_code'])
        return {
            'vehicle': vehicle,
            'mileage_date': timezone.now().strftime('%Y-%m-%d'),
            'mileage': vehicle.vehicle_mileage,
        }


class MileageEditView(LoginRequiredMixin, TitleMixin, SuccessUrlMixin,
                      UpdateView):
    model = MileageEvent
    fields = ['vehicle', 'mileage_date', 'mileage']
    title = 'Edit mileage event'


class MileageDeleteView(LoginRequiredMixin, SuccessUrlMixin, TitleMixin,
                        DeleteView):
    model = MileageEvent
    title = 'Mileage event deletion'


class MileageListView(LoginRequiredMixin, TitleMixin, ListView):
    model = MileageEvent
    title = 'Mileage Events list'
