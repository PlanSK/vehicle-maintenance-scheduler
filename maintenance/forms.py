from django import forms

from maintenance.models import Event, MileageEvent


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
