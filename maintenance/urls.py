"""
URL configuration for vehicle_scheduler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from . import views


urlpatterns = [
    path('', views.VehicleListView.as_view(), name="index"),
    path('login/', views.LoginUser.as_view(), name="login"),
# Vehicle section
    path('add_vehicle/', views.VehicleCreateView.as_view(), name="add_vehicle"),
    path('vehicle/<str:vin_code>/', views.VehicleDetailView.as_view(), name="vehicle_detail"),
    path('edit_vehicle/<int:pk>/', views.VehicleEditView.as_view(), name="edit_vehicle"),
    path('delete_vehicle/<int:pk>/', views.VehicleDeleteView.as_view(), name="delete_vehicle"),
# Work section
    path('add_work/<str:vin_code>/', views.WorkCreateView.as_view(), name="add_work"),
    path('edit_work/<int:pk>/', views.WorkEditView.as_view(), name="edit_work"),
    path('delete_work/<int:pk>/', views.WorkDeleteView.as_view(), name="delete_work"),
    path('list_of_works/<str:vin_code>/', views.WorkListView.as_view(), name="list_of_works"),
    path('work_detail/<int:pk>/', views.WorkDetailView.as_view(), name="work_detail"),
# Event section
    path('add_event/<str:vin_code>/', views.EventCreateView.as_view(), name="add_event"),
    path('edit_event/<int:pk>/', views.EventEditView.as_view(), name="edit_event"),
    path('delete_event/<int:pk>/', views.EventDeleteView.as_view(), name="delete_event"),
    path('events_list/', views.EventListView.as_view(), name="events_list"),
    path('event_detail/<int:pk>/', views.EventDetailView.as_view(), name="event_detail"),
# Mileage events section
    path('add_mileage/<str:vin_code>/', views.MileageCreateView.as_view(), name="add_mileage"),
    path('edit_mileage/<int:pk>/', views.MileageEditView.as_view(), name="edit_mileage"),
    path('delete_mileage/<int:pk>/', views.MileageDeleteView.as_view(), name="delete_mileage"),
    path('mileage_events_list/', views.MileageListView.as_view(), name="mileage_events_list"),
]
