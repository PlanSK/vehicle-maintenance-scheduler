from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='vehicles')
    vin_code = models.CharField(
        max_length=17, verbose_name='VIN', unique=True,
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9]{9}[a-zA-Z0-9-]{2}[0-9]{6}')
        ])
    vehicle_manufacturer = models.CharField(max_length=50,
                                            verbose_name='Manufacturer')
    vehicle_model = models.CharField(max_length=20, verbose_name='Model')
    vehicle_body = models.CharField(max_length=10, verbose_name='Body')
    vehicle_year = models.IntegerField(verbose_name='Year')
    vehicle_mileage = models.IntegerField(verbose_name='Mileage')

    def __str__(self) -> str:
        return ' '.join((self.vehicle_manufacturer, self.vehicle_model,
                         self.vehicle_body, str(self.vehicle_year)))

    def save(self, *args, **kwargs) -> None:
        self.vin_code = self.vin_code.upper()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('vehicle_detail',
                            kwargs={'vin_code': self.vin_code})


class Work(models.Model):
    class WorkType(models.TextChoices):
        REPAIR = 'REPAIR', 'Repair'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'
        TUNING = 'TUNING', 'Tuning'

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                related_name='works_list')
    work_type = models.CharField(
        max_length=20, choices=WorkType.choices, default=WorkType.MAINTENANCE,
        verbose_name='Work Type')
    title = models.CharField(max_length=255, verbose_name='Title')
    interval_month = models.IntegerField(verbose_name='Interval in month',
                                         null=True, blank=True)
    interval_km = models.IntegerField(verbose_name='Interval in kilometers',
                                      null=True, blank=True)
    note = models.CharField(max_length=255, verbose_name='Note', blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('work_detail', kwargs={'pk': self.pk})


class Event(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                related_name='events', verbose_name='Vehicle')
    work_date = models.DateField(verbose_name='Event Date')
    mileage = models.IntegerField(verbose_name='Mileage')
    work = models.ForeignKey(Work, on_delete=models.CASCADE,
                             related_name='work', verbose_name='Work title')
    part_price = models.FloatField(verbose_name='Part price', default=0.0)
    work_price = models.FloatField(verbose_name='Work price', default=0.0)
    note = models.CharField(max_length=255, verbose_name='Note', blank=True)

    class Meta:
        ordering = ['-work_date']

    def __str__(self) -> str:
        return f'{self.work_date} {self.work} ({self.mileage})'

    def get_absolute_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs) -> None:
        if self.mileage > self.vehicle.vehicle_mileage:
            self.vehicle.vehicle_mileage = self.mileage 
            self.vehicle.save()
        return super().save(*args, **kwargs)


class MileageEvent(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                related_name='mileage_events',
                                verbose_name='Vehicle')
    mileage_date = models.DateField(verbose_name='Mileage Date')
    mileage = models.IntegerField(verbose_name='Mileage')

    def __str__(self) -> str:
        return f'{self.mileage_date} {self.vehicle} ({self.mileage})'
    
    def save(self, *args, **kwargs) -> None:
        if self.mileage > self.vehicle.vehicle_mileage:
            self.vehicle.vehicle_mileage = self.mileage 
            self.vehicle.save()
        return super().save(*args, **kwargs)
