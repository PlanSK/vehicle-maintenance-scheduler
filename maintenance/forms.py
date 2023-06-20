from django import forms

from maintenance.models import Event, MileageEvent, Vehicle, Work


class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'work_date': DateInput(),
            'vehicle': forms.HiddenInput(),
        }


class MileageEventForm(forms.ModelForm):
    class Meta:
        model = MileageEvent
        fields = '__all__'
        widgets = {
            'mileage_date': DateInput(),
            'vehicle': forms.HiddenInput(),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'owner': forms.HiddenInput(),
        }


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'
        widgets = {
            'vehicle': forms.HiddenInput(),
        }
